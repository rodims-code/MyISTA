# 👥 MyISTA – Feature « Groupes de travail »

> Document de spécification destiné à un **agent IA développeur**.
> Il décrit TOUT ce qu'il faut construire (backend Django/DRF + frontend SvelteKit) pour la feature **Groupes de travail**. Respecte la stack et la structure existantes décrites dans le `README.md` principal du projet.

---

## 📌 Table des matières

1. [Contexte & objectif](#1--contexte--objectif)
2. [Périmètre (inclus / exclu)](#2--périmètre)
3. [Stack & conventions](#3--stack--conventions)
4. [Concepts métier](#4--concepts-métier)
5. [Rôles & permissions](#5--rôles--permissions)
6. [Règles métier](#6--règles-métier)
7. [Modèle de données (Django)](#7--modèle-de-données-django)
8. [API REST (DRF)](#8--api-rest-drf)
9. [Sécurité & filtrage backend](#9--sécurité--filtrage-backend)
10. [Export PDF](#10--export-pdf)
11. [Frontend (SvelteKit)](#11--frontend-sveltekit)
12. [Maquettes UI](#12--maquettes-ui)
13. [Tests](#13--tests)
14. [Plan d'implémentation](#14--plan-dimplémentation-ordre-conseillé)
15. [Critères d'acceptation](#15--critères-dacceptation-definition-of-done)
16. [Hors MVP / évolutions](#16--hors-mvp--évolutions)

---

## 1. 🎯 Contexte & objectif

À l'ISTA, les professeurs donnent leurs TP **hors de MyISTA** (PDF, photo du tableau, document WhatsApp). Les étudiants se débrouillent ensuite dans des groupes WhatsApp où les fichiers se perdent.

**Principe de la feature :**

> MyISTA ne gère **pas** le professeur. Il permet aux étudiants de transformer un TP reçu physiquement ou par WhatsApp en **espace de travail organisé pour leur classe**.

Les professeurs **ne créent pas de compte** et ne changent pas leurs habitudes. Un étudiant importe le sujet dans MyISTA, crée un groupe, invite ses camarades (qui rejoignent eux-mêmes), puis le groupe rédige le compte rendu et l'exporte en PDF.

---

## 2. 📦 Périmètre

### ✅ Inclus (MVP de la feature)

- Groupes **liés à une classe** (`niveau` + `filiere`), visibles uniquement par les étudiants de cette classe
- Création de groupe → le créateur devient **chef (leader)** automatiquement
- Rejoindre / quitter un groupe (limite de membres)
- Gestion de base par le chef : modifier le groupe, retirer un membre, transférer le leadership, supprimer le groupe
- **TP (Assignment)** : titre + sujet (PDF ou photo) importé par un étudiant
- **Fichiers du groupe** : upload, liste, téléchargement, suppression
- **Document de travail (Workspace)** : sections éditables, sauvegarde manuelle, contrôle de concurrence simple
- **Export PDF** du document de travail
- Filtrage **côté backend** (Django/DRF), pas seulement dans l'UI

### ❌ Exclu (ne PAS implémenter)

- Comptes/rôles professeur dans cette feature
- Collaboration temps réel (WebSocket, CRDT, curseurs)
- Notifications push, mentions
- Chat : le **chat entre étudiants existe déjà** dans MyISTA. Ne pas le recréer ni le modifier dans cette feature. Aucun chat spécifique au groupe n'est développé ici ; le brancher sur les groupes est une évolution ultérieure (§16), en réutilisant le module existant
- Demandes d'adhésion avec validation par le chef (on rejoint directement)
- Invitations par lien/code
- IA / agent automatique, OCR des photos
- Historique/versions complet du document

---

## 3. 🛠️ Stack & conventions

| Couche | Technologie |
|--------|-------------|
| Frontend | SvelteKit, TypeScript, TailwindCSS, DaisyUI |
| Tests front | Vitest (unit + component) |
| Backend | Django, Django REST Framework, JWT (SimpleJWT) |
| BDD | SQLite (dev) / PostgreSQL (prod) |
| Fichiers | Stockage local (`MEDIA_ROOT`) — abstrait pour migrer vers S3 plus tard |
| PDF | WeasyPrint (HTML → PDF) *(fallback : ReportLab)* |

### Conventions générales

- **Langue de l'UI : français.** Code, noms de variables, modèles et endpoints : **anglais** (comme dans les specs ci-dessous).
- Backend : une **app Django dédiée** `groups` (`backend/groups/`) avec `models.py`, `serializers.py`, `views.py`, `permissions.py`, `urls.py`, `services.py`, `tests/`.
- Frontend : respecter l'arborescence existante `src/lib/{components,layout,api,stores}` et `src/routes/app/*`.
- TypeScript strict : aucun `any` ; typer toutes les réponses API.
- Utiliser les classes **DaisyUI** (`btn`, `card`, `badge`, `modal`, `tabs`, `alert`, `skeleton`, `toast`) avant d'écrire du CSS custom.
- Réutiliser le client API existant (`src/lib/api`) et le store d'authentification (JWT + user). Ne pas dupliquer la logique d'auth.
- Commits atomiques, un commit par étape du plan (section 14).

---

## 4. 🧠 Concepts métier

Trois notions à **ne pas confondre** :

| Concept | Description | Modèle |
|---------|-------------|--------|
| 📚 **TP** | Le sujet donné par le professeur (PDF/photo) | `Assignment` |
| 👥 **Groupe** | Les étudiants qui travaillent dessus | `Group`, `GroupMember` |
| 📝 **Travail** | Le document que les étudiants construisent | `Workspace`, `WorkspaceSection` |

```text
Group (L1 — Électricité)
│
├── Assignment (le TP)
│     └── subject_file (Sujet.pdf / photo)
│
├── Members (👑 leader + members)
│
├── Files (GroupFile : calculs.pdf, montage.jpg, mesures.xlsx)
│
└── Workspace (document de travail)
      └── Sections (Introduction, Objectif, Matériel, ...)
            └── Export PDF
```

**Relation :** un `Group` a **au plus un** `Assignment` et **un seul** `Workspace` (créé automatiquement avec le groupe). Un étudiant peut appartenir à **plusieurs** groupes de sa classe (ex. un par TP).

---

## 5. 🔐 Rôles & permissions

Rôle **global** (existant) : `student`, `delegate`, `professor`, `admin`.
Rôle **dans un groupe** : `leader`, `member`.

> Dans cette feature, seuls `student` et `delegate` (traités comme des étudiants) interagissent. `admin` a un accès lecture/suppression de modération. `professor` : aucun accès dans le MVP.

| Action | Étudiant même classe (non membre) | Membre | Chef | Admin |
|--------|:--:|:--:|:--:|:--:|
| Lister les groupes de sa classe | ✅ | ✅ | ✅ | ✅ (toutes) |
| Voir le détail d'un groupe (aperçu : nom, description, chef, nb membres) | ✅ | ✅ | ✅ | ✅ |
| Voir contenu complet (fichiers, workspace, sujet) | ❌ | ✅ | ✅ | ✅ |
| Créer un groupe | ✅ | — | — | ❌ |
| Rejoindre | ✅ (si place dispo) | — | — | ❌ |
| Quitter | — | ✅ | ✅ (avec règle §6) | ❌ |
| Éditer le workspace | ❌ | ✅ | ✅ | ❌ |
| Uploader un fichier / le TP | ❌ | ✅ | ✅ | ❌ |
| Supprimer un fichier | ❌ | Ses propres fichiers | Tous | ✅ |
| Modifier le groupe (nom, description, max) | ❌ | ❌ | ✅ | ✅ |
| Retirer un membre | ❌ | ❌ | ✅ | ✅ |
| Transférer le leadership | ❌ | ❌ | ✅ | ❌ |
| Supprimer le groupe | ❌ | ❌ | ✅ | ✅ |
| Exporter en PDF | ❌ | ✅ | ✅ | ✅ |

Un étudiant d'une **autre classe** n'a **aucun accès**, pas même à l'aperçu → réponse **404** (pas 403, pour ne pas révéler l'existence).

---

## 6. 📏 Règles métier

1. **Appartenance à une classe** : un groupe a un `niveau` + `filiere`, **copiés depuis le créateur** à la création et **immuables** ensuite. Seuls les étudiants avec les mêmes valeurs voient/rejoignent le groupe.
2. **Création** : le créateur devient automatiquement `GroupMember(role=leader)` ; `Group.created_by` = créateur. Un `Workspace` vide avec sections par défaut est créé dans la même transaction.
3. **Sections par défaut** du workspace (ordre) : `Introduction`, `Objectif`, `Matériel`, `Manipulation`, `Résultats`, `Conclusion`.
4. **`max_members`** : entier entre **2 et 10**, défaut **5**. Ne peut pas être réduit en dessous du nombre actuel de membres.
5. **Rejoindre** : refusé si groupe plein (`409`), si déjà membre (`409`), ou si classe différente (`404`).
6. **Un seul chef** par groupe, toujours.
7. **Quitter** :
   - Un `member` peut quitter librement.
   - Le `leader` qui quitte doit d'abord **transférer le leadership** ; sinon, s'il est **seul** dans le groupe, le groupe est **supprimé** ; s'il reste d'autres membres et aucun transfert n'est fourni → `400` (`LEADER_MUST_TRANSFER`).
8. **Retirer un membre** : seul le chef ; il ne peut pas se retirer lui-même via cet endpoint (utiliser « quitter »).
9. **Suppression du groupe** : supprime en cascade membres, fichiers (**y compris les fichiers physiques sur disque**), assignment, workspace.
10. **Fichiers** : taille max **10 Mo** ; extensions autorisées : `pdf, jpg, jpeg, png, webp, doc, docx, xls, xlsx, ppt, pptx, txt, csv, zip`. Valider extension **et** type MIME. Maximum **30 fichiers** par groupe.
11. **TP (Assignment)** : titre obligatoire (≤ 150 car.), sujet = 1 fichier (`pdf`, `jpg`, `jpeg`, `png`, `webp`). Peut être créé à la création du groupe ou ajouté/remplacé plus tard par n'importe quel membre.
12. **Workspace – concurrence** : chaque section a un champ `version` (entier). Une mise à jour doit envoyer la `version` connue ; si elle diffère de celle en base → `409 CONFLICT` avec la version actuelle de la section, pour que le front propose « Recharger » ou « Écraser ». Pas de temps réel.
13. **Contenu des sections** : texte brut / Markdown simple (titres, gras, listes). Max **20 000 caractères** par section. Le rendu PDF doit **assainir** le contenu (pas de HTML brut non échappé).
14. **Noms** : `name` ≤ 80 car., unique **par classe** (insensible à la casse) pour éviter la confusion.

---

## 7. 🗃️ Modèle de données (Django)

Fichier : `backend/groups/models.py`. L'utilisateur est `settings.AUTH_USER_MODEL` (champs existants : `matricule`, `pseudo`, `niveau`, `filiere`, `role`).

```python
import uuid
from django.conf import settings
from django.db import models
from django.db.models.functions import Lower

User = settings.AUTH_USER_MODEL


class Group(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=80)
    description = models.TextField(blank=True, max_length=500)
    niveau = models.CharField(max_length=20)      # copié du créateur, immuable
    filiere = models.CharField(max_length=60)     # copié du créateur, immuable
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="created_groups")
    max_members = models.PositiveSmallIntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["niveau", "filiere"])]
        constraints = [
            models.UniqueConstraint(
                Lower("name"), "niveau", "filiere", name="uniq_group_name_per_class"
            ),
            models.CheckConstraint(
                check=models.Q(max_members__gte=2, max_members__lte=10),
                name="group_max_members_range",
            ),
        ]


class GroupMember(models.Model):
    class Role(models.TextChoices):
        LEADER = "leader", "Chef"
        MEMBER = "member", "Membre"

    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="memberships")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="group_memberships")
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.MEMBER)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["group", "user"], name="uniq_member_per_group"),
            # un seul chef par groupe
            models.UniqueConstraint(
                fields=["group"],
                condition=models.Q(role="leader"),
                name="uniq_leader_per_group",
            ),
        ]
        ordering = ["role", "joined_at"]  # leader d'abord ('leader' < 'member')


class Assignment(models.Model):
    """Le TP : sujet donné par le professeur, importé par un étudiant."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    group = models.OneToOneField(Group, on_delete=models.CASCADE, related_name="assignment")
    title = models.CharField(max_length=150)
    subject_file = models.FileField(upload_to="groups/subjects/%Y/%m/")
    subject_type = models.CharField(max_length=10)  # pdf | image
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class GroupFile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="files")
    name = models.CharField(max_length=150)           # nom affiché
    file = models.FileField(upload_to="groups/files/%Y/%m/")
    file_type = models.CharField(max_length=10)       # extension normalisée
    size = models.PositiveIntegerField()              # octets
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]


class Workspace(models.Model):
    group = models.OneToOneField(Group, on_delete=models.CASCADE, related_name="workspace")
    title = models.CharField(max_length=150, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)


class WorkspaceSection(models.Model):
    id = models.BigAutoField(primary_key=True)
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name="sections")
    title = models.CharField(max_length=100)
    content = models.TextField(blank=True, max_length=20000)
    order = models.PositiveSmallIntegerField(default=0)
    version = models.PositiveIntegerField(default=1)  # concurrence optimiste
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ["order", "id"]
```

**Notes d'implémentation**

- Ajouter des **signaux** (ou la logique dans `services.py`) pour supprimer les fichiers physiques à la suppression d'un `GroupFile`/`Assignment`/`Group`.
- Toute la logique métier multi-étapes (créer groupe + chef + workspace, transférer leadership, quitter) va dans `services.py` avec `@transaction.atomic` et `select_for_update()` sur le groupe pour éviter les dépassements de `max_members` en concurrence.
- Générer et appliquer les migrations (`makemigrations groups && migrate`).

---

## 8. 🌐 API REST (DRF)

Préfixe : `/api/groups/`. Authentification : JWT (`Authorization: Bearer <token>`) obligatoire partout. Pagination `PageNumberPagination` (page_size 20) sur les listes. Format d'erreur uniforme :

```json
{ "code": "GROUP_FULL", "detail": "Ce groupe est complet." }
```

### 8.1 Groupes

| Méthode | URL | Description | Perm. |
|---------|-----|-------------|-------|
| GET | `/api/groups/` | Groupes de ma classe (`?mine=true` : seulement ceux où je suis membre ; `?search=`) | Étudiant |
| POST | `/api/groups/` | Créer un groupe (+ TP optionnel) | Étudiant |
| GET | `/api/groups/{id}/` | Détail (aperçu si non membre, complet si membre) | Même classe |
| PATCH | `/api/groups/{id}/` | Modifier `name`, `description`, `max_members` | Chef |
| DELETE | `/api/groups/{id}/` | Supprimer le groupe | Chef / Admin |
| POST | `/api/groups/{id}/join/` | Rejoindre | Même classe |
| POST | `/api/groups/{id}/leave/` | Quitter. Body optionnel : `{ "new_leader_id": 12 }` | Membre |

**`GET /api/groups/` – réponse (item)**

```json
{
  "id": "6f1c…",
  "name": "Les Électrons ⚡",
  "description": "Groupe de travail pour les TP d'électricité.",
  "niveau": "L1",
  "filiere": "Électricité",
  "leader": { "id": 3, "pseudo": "Dieuveil" },
  "members_count": 4,
  "max_members": 5,
  "is_full": false,
  "is_member": false,
  "my_role": null,
  "assignment_title": "TP — Étude d'un moteur asynchrone",
  "created_at": "2026-03-20T21:14:00Z"
}
```

**`POST /api/groups/`** (JSON ou `multipart/form-data` si sujet joint)

```json
{
  "name": "Les Électrons ⚡",
  "description": "Groupe de travail pour les TP d'électricité.",
  "max_members": 5,
  "assignment_title": "TP — Étude d'un moteur asynchrone",
  "subject_file": "<fichier optionnel>"
}
```

→ `201` avec le détail complet du groupe. `niveau`/`filiere` ne sont **jamais** acceptés du client : ils viennent de `request.user`.

**`GET /api/groups/{id}/` – membre (détail complet)** ajoute :

```json
{
  "members": [
    { "id": 3, "pseudo": "Dieuveil", "role": "leader", "joined_at": "…" },
    { "id": 8, "pseudo": "Patrick", "role": "member", "joined_at": "…" }
  ],
  "assignment": {
    "id": "…", "title": "…", "subject_url": "/media/…", "subject_type": "pdf",
    "uploaded_by": { "id": 3, "pseudo": "Dieuveil" }
  },
  "files_count": 3
}
```

Pour un non-membre : seulement les champs de la liste (`members`, `assignment.subject_url`, fichiers **non exposés**).

### 8.2 Membres

| Méthode | URL | Description | Perm. |
|---------|-----|-------------|-------|
| GET | `/api/groups/{id}/members/` | Liste des membres | Membre |
| DELETE | `/api/groups/{id}/members/{user_id}/` | Retirer un membre | Chef / Admin |
| POST | `/api/groups/{id}/transfer-leadership/` | Body `{ "user_id": 8 }` | Chef |

### 8.3 TP (Assignment)

| Méthode | URL | Description | Perm. |
|---------|-----|-------------|-------|
| PUT | `/api/groups/{id}/assignment/` | Créer ou remplacer le TP (`multipart`: `title`, `subject_file`) | Membre |
| GET | `/api/groups/{id}/assignment/` | Lire le TP | Membre |
| DELETE | `/api/groups/{id}/assignment/` | Supprimer le TP | Chef |

### 8.4 Fichiers du groupe

| Méthode | URL | Description | Perm. |
|---------|-----|-------------|-------|
| GET | `/api/groups/{id}/files/` | Liste | Membre |
| POST | `/api/groups/{id}/files/` | Upload (`multipart`: `file`, `name` optionnel) | Membre |
| GET | `/api/groups/{id}/files/{file_id}/download/` | Téléchargement **contrôlé** (vérifie l'appartenance) | Membre |
| DELETE | `/api/groups/{id}/files/{file_id}/` | Supprimer | Auteur / Chef / Admin |

> ⚠️ Ne **jamais** servir les fichiers de groupe via une URL `/media/` publique. Utiliser la vue `download/` qui vérifie la permission puis renvoie un `FileResponse`. Même chose pour `subject_url` : exposer une URL passant par une vue protégée (`/api/groups/{id}/assignment/subject/`).

### 8.5 Workspace

| Méthode | URL | Description | Perm. |
|---------|-----|-------------|-------|
| GET | `/api/groups/{id}/workspace/` | Titre + sections | Membre |
| PATCH | `/api/groups/{id}/workspace/` | Modifier le titre du document | Membre |
| POST | `/api/groups/{id}/workspace/sections/` | Ajouter une section `{title, order?}` | Membre |
| PATCH | `/api/groups/{id}/workspace/sections/{section_id}/` | Modifier `{title?, content?, version}` | Membre |
| DELETE | `/api/groups/{id}/workspace/sections/{section_id}/` | Supprimer une section | Membre |
| POST | `/api/groups/{id}/workspace/sections/reorder/` | `{ "order": [id1, id2, …] }` | Membre |
| GET | `/api/groups/{id}/workspace/export-pdf/` | Télécharge le PDF | Membre |

**`PATCH …/sections/{id}/`**

```json
{ "content": "Le moteur asynchrone…", "version": 3 }
```

- Succès → `200` avec la section (version incrémentée à 4, `updated_by` = user courant).
- Version obsolète → `409` :

```json
{
  "code": "SECTION_CONFLICT",
  "detail": "Cette section a été modifiée par un autre membre.",
  "current": { "id": 5, "content": "…", "version": 4, "updated_by": { "pseudo": "Patrick" } }
}
```

L'incrément se fait avec un `UPDATE … WHERE id=… AND version=…` (ou `F('version') + 1` filtré) pour être atomique.

### 8.6 Codes d'erreur à implémenter

`GROUP_FULL` (409), `ALREADY_MEMBER` (409), `NOT_MEMBER` (403), `NOT_LEADER` (403), `LEADER_MUST_TRANSFER` (400), `INVALID_FILE_TYPE` (400), `FILE_TOO_LARGE` (400), `FILE_LIMIT_REACHED` (400), `MAX_BELOW_MEMBERS` (400), `DUPLICATE_NAME` (400), `SECTION_CONFLICT` (409).

---

## 9. 🛡️ Sécurité & filtrage backend

**Règle d'or : le filtrage par classe se fait dans Django, jamais uniquement dans l'UI.**

### Queryset de base

```python
# backend/groups/views.py
def visible_groups(user):
    qs = Group.objects.select_related("created_by").prefetch_related("memberships__user")
    if user.role == "admin":
        return qs
    return qs.filter(niveau=user.niveau, filiere=user.filiere)
```

Toutes les vues (`get_queryset`) partent de `visible_groups(request.user)`. Résultat : un `GET /api/groups/<id d'une autre classe>/` renvoie **404**.

### Permissions DRF (`permissions.py`)

- `IsStudentOrAdmin` : `role in {student, delegate, admin}`.
- `IsGroupMember` : l'utilisateur a un `GroupMember` sur ce groupe (ou est admin pour les actions autorisées).
- `IsGroupLeader` : `role == leader`.
- Les objets liés (`files`, `assignment`, `workspace`) vérifient la permission via **le groupe parent** — ne jamais faire confiance à un `file_id` seul : toujours `get_object_or_404(GroupFile, id=file_id, group=group)`.

### Autres exigences

- Valider les uploads : extension, MIME réel (`python-magic` ou `imghdr`/`filetype`), taille, nom assaini (`get_valid_filename`), nom de stockage aléatoire (UUID).
- Throttling DRF sur création de groupe (ex. 10/heure/utilisateur) et upload (ex. 60/heure).
- Échapper le contenu avant rendu PDF (voir §10).
- Ne pas exposer l'email/matricule des membres : seulement `id` et `pseudo`.

---

## 10. 📄 Export PDF

Endpoint : `GET /api/groups/{id}/workspace/export-pdf/`

- Génère un PDF A4 via **WeasyPrint** à partir d'un template Django HTML (`groups/templates/groups/export.html`).
- Contenu : en-tête (ISTA / MyISTA, classe `L1 — Électricité`, nom du groupe, titre du TP, date d'export), liste des membres (chef marqué 👑 ou « (chef) »), puis chaque section : `<h2>titre</h2>` + contenu rendu.
- Le Markdown est converti en HTML avec `markdown` + **nettoyage `bleach`** (balises autorisées : `p, br, strong, em, ul, ol, li, h3, h4, code, pre, blockquote`).
- Nom du fichier (header `Content-Disposition`) :
  `TP_{slug(assignment.title)}_{niveau}_{filiere}_{slug(group.name)}.pdf`
  ex. `TP_Moteur_Asynchrone_L1_Electricite_Les_Electrons.pdf`
- Si une section est vide : afficher « — Non renseigné — ».
- Les images du groupe **ne sont pas** intégrées automatiquement dans le MVP (hors périmètre).
- Prévoir un test qui vérifie `Content-Type: application/pdf` et que la réponse commence par `%PDF`.

---

## 11. 🖥️ Frontend (SvelteKit)

### 11.1 Routes (ajouts dans la zone protégée)

```text
src/routes/app/groupes/
├── +page.svelte                 # Liste des groupes de ma classe + bouton « Créer un groupe »
├── +page.ts                     # (optionnel) load
├── nouveau/
│   └── +page.svelte             # Formulaire de création (ou modal depuis la liste)
└── [id]/
    ├── +layout.svelte           # En-tête du groupe + onglets
    ├── +layout.ts               # load : détail du groupe (gère 404/403)
    ├── +page.svelte             # Vue d'ensemble (sujet + membres + résumé)
    ├── travail/+page.svelte     # Workspace (sections éditables)
    ├── fichiers/+page.svelte    # Fichiers du groupe
    └── membres/+page.svelte     # Membres + actions chef
```

Ajouter l'entrée **« Groupes » (icône 👥)** dans la sidebar du dashboard, entre « Documents » et « Infos ». Route protégée par le garde existant de `/app/*`.

### 11.2 Services API — `src/lib/api/groups.ts`

Fonctions typées (utiliser le client fetch existant avec JWT) :

```ts
listGroups(params?: { mine?: boolean; search?: string; page?: number })
getGroup(id: string)
createGroup(payload: CreateGroupPayload)           // FormData si sujet joint
updateGroup(id: string, payload: Partial<GroupUpdate>)
deleteGroup(id: string)
joinGroup(id: string)
leaveGroup(id: string, newLeaderId?: number)
listMembers(id: string)
removeMember(id: string, userId: number)
transferLeadership(id: string, userId: number)
putAssignment(id: string, payload: { title: string; subject_file: File })
deleteAssignment(id: string)
listFiles(id: string)
uploadFile(id: string, file: File, name?: string)
deleteFile(id: string, fileId: string)
downloadFile(id: string, fileId: string)           // blob avec JWT
getWorkspace(id: string)
updateWorkspaceTitle(id: string, title: string)
createSection(id: string, title: string)
updateSection(id: string, sectionId: number, data: { title?: string; content?: string; version: number })
deleteSection(id: string, sectionId: number)
reorderSections(id: string, order: number[])
exportWorkspacePdf(id: string)                     // blob → téléchargement
```

Types dans `src/lib/api/types/groups.ts` : `Group`, `GroupDetail`, `GroupMember`, `Assignment`, `GroupFile`, `Workspace`, `WorkspaceSection`, `ApiError { code: string; detail: string; current?: WorkspaceSection }`.

Les fichiers protégés (sujet, téléchargements, PDF) se récupèrent en `blob` avec le header `Authorization`, puis `URL.createObjectURL` (prévisualisation PDF/image) ou téléchargement.

### 11.3 Stores — `src/lib/stores/groups.ts`

- `currentGroup` (writable<GroupDetail | null>) — alimenté par `+layout.ts`.
- `myRoleInGroup` (derived) → `'leader' | 'member' | null`.
- `workspaceStore` : sections, état `dirty` par section, état de sauvegarde (`idle | saving | saved | conflict | error`).
- Ne pas dupliquer l'utilisateur : lire depuis le store d'auth existant.

### 11.4 Composants — `src/lib/components/groups/`

| Composant | Rôle |
|-----------|------|
| `GroupCard.svelte` | Carte (nom, description, TP, `x / y membres`, chef 👑, bouton **Rejoindre / Complet / Ouvrir**) |
| `GroupList.svelte` | Grille + états chargement (`skeleton`), vide, erreur |
| `CreateGroupForm.svelte` | Nom, description, max membres (2–10), TP optionnel (titre + PDF/photo), validation |
| `MemberList.svelte` | Liste avec 👑 / 👤, actions chef (retirer, transférer) via modal de confirmation |
| `AssignmentCard.svelte` | Titre du TP + prévisualisation/téléchargement du sujet + remplacer |
| `FileUploader.svelte` | Drag & drop + bouton, progression, validation taille/type côté client |
| `FileList.svelte` | Icônes par type (📄 📷 📊), taille, auteur, télécharger, supprimer |
| `WorkspaceSection.svelte` | Titre + zone texte (`textarea`) en mode lecture/édition, bouton Enregistrer, gestion du conflit |
| `ConflictModal.svelte` | Affiche la version du serveur ; actions **Recharger** / **Écraser** |
| `ConfirmModal.svelte` | Confirmation générique (quitter, supprimer, retirer) — réutiliser s'il existe déjà |
| `ExportPdfButton.svelte` | Appelle l'export, état de chargement, toast d'erreur |

Utiliser les composants globaux existants (toasts, layout) ; créer seulement ce qui manque.

### 11.5 Comportements UX attendus

- **Liste** : onglets `Tous les groupes` / `Mes groupes`. Champ de recherche. Le bouton **Rejoindre** est désactivé et devient **Complet** si `is_full`.
- **Rejoindre** : mise à jour optimiste du compteur, rollback + toast si erreur (`GROUP_FULL`, `ALREADY_MEMBER`).
- **Non-membre** sur `/app/groupes/[id]` : voir l'aperçu (description, chef, membres count) + bouton Rejoindre ; les onglets Travail / Fichiers / Membres sont masqués ou verrouillés.
- **Workspace** : chaque section s'édite individuellement (`Modifier` → textarea → `Enregistrer` / `Annuler`). Avertir avant de quitter la page si une section est `dirty` (`beforeNavigate`). Afficher « Dernière modification par *Patrick* · il y a 5 min ». Sur `409`, ouvrir `ConflictModal`.
- **Quitter (chef)** : si d'autres membres existent, modal « Choisir le nouveau chef » avant de confirmer.
- **Erreurs** : mapper les `code` API vers des messages français clairs (fichier `src/lib/api/errors.ts`).
- **Responsive** : mobile-first (les étudiants utilisent surtout leur téléphone). Onglets du groupe en haut, scrollables horizontalement.
- **Accessibilité** : labels sur tous les champs, focus visible, boutons icône avec `aria-label`.

### 11.6 Libellés (français)

`Groupes de travail`, `Créer un groupe`, `Rejoindre`, `Complet`, `Quitter le groupe`, `Chef du groupe`, `Membres`, `Fichiers du groupe`, `Travail`, `Sujet`, `Modifier`, `Enregistrer`, `Exporter en PDF`, `Nouveau travail`, `Ajouter un PDF`, `Prendre une photo`.

---

## 12. 🎨 Maquettes UI

**Liste des groupes**

```text
👥 Groupes de travail
L1 — Électricité                         [ + Créer un groupe ]
[ Tous les groupes | Mes groupes ]   🔍 Rechercher…

┌─────────────────────────┐  ┌─────────────────────────┐
│ ⚡ Les Électrons         │  │ ⚡ Groupe 2              │
│ TP Machines électriques │  │ TP Électricité générale │
│ 4 / 5 membres           │  │ 5 / 5 membres           │
│ 👑 Dieuveil             │  │ 👑 Patrick              │
│ [ Rejoindre ]           │  │ [ Complet ]             │
└─────────────────────────┘  └─────────────────────────┘
```

**Création**

```text
Nom du groupe        [ Les Électrons ⚡          ]
Description          [ Groupe de travail pour…  ]
Maximum de membres   [ 5 ▾ ]
── TP (optionnel, modifiable plus tard) ──
Titre                [ TP 03 — Machines électriques ]
Sujet                [ 📎 Ajouter un PDF ] [ 📷 Prendre une photo ]
                                     [ Créer le groupe ]
```

**Détail du groupe (membre)**

```text
┌──────────────────────────────────────────┐
│ 👥 Les Électrons          L1 Électricité │
│ [ Aperçu | Travail | Fichiers | Membres ]│
├──────────────────────────────────────────┤
│ 📄 Sujet : TP_Moteur_Asynchrone.pdf      │
│ 👥 Membres : 👑 Dieuveil 👤 Patrick …    │
│ 📝 Travail                               │
│   Introduction            [ Modifier ]   │
│   1. Objectif             [ Modifier ]   │
│   …                                      │
│ 📎 Fichiers : calculs.pdf, montage.jpg   │
│              📄 Exporter en PDF          │
└──────────────────────────────────────────┘
```

---

## 13. ✅ Tests

### Backend (`backend/groups/tests/`, `pytest-django` ou `TestCase`)

Couvrir au minimum :

- **Visibilité** : un étudiant L1-Mécanique ne voit pas et n'accède pas (404) aux groupes de L1-Électricité ; admin voit tout.
- **Création** : le créateur est `leader`, `niveau/filiere` copiés de l'utilisateur (ignorer toute valeur envoyée), workspace + 6 sections par défaut créés.
- **Rejoindre** : OK, groupe plein, déjà membre, autre classe.
- **Concurrence** : deux `join` simultanés sur la dernière place → un seul succès.
- **Quitter** : membre OK ; chef seul → groupe supprimé ; chef avec membres sans transfert → 400 ; avec transfert → nouveau chef.
- **Permissions** : non-membre refusé sur files/workspace/export ; membre non-chef refusé sur PATCH/DELETE groupe ; chef peut retirer un membre.
- **Fichiers** : type invalide, taille > 10 Mo, limite 30, téléchargement protégé, suppression du fichier physique.
- **Workspace** : mise à jour avec bonne version → incrément ; mauvaise version → 409 avec `current`.
- **Export PDF** : `application/pdf`, commence par `%PDF`, contenu HTML malveillant neutralisé.
- **Contraintes DB** : unicité du nom par classe (casse ignorée), un seul chef.

### Frontend (Vitest + @testing-library/svelte)

- `GroupCard` : états Rejoindre / Complet / Ouvrir.
- `CreateGroupForm` : validation (nom requis, max 2–10, fichier type/taille).
- `WorkspaceSection` : édition, état `dirty`, ouverture de `ConflictModal` sur 409.
- `FileUploader` : rejet côté client des fichiers trop gros ou de mauvais type.
- Service `groups.ts` : mock de `fetch`, vérification des URLs, headers JWT et mapping des erreurs.

---

## 14. 🧭 Plan d'implémentation (ordre conseillé)

1. **Backend – modèles & migrations** (§7) + contraintes.
2. **Backend – services & permissions** (§9) : `visible_groups`, `IsGroupMember`, `IsGroupLeader`, logique transactionnelle.
3. **Backend – API groupes + membres** (join/leave/transfer/remove) + tests.
4. **Backend – TP + fichiers** (upload validé, téléchargement protégé) + tests.
5. **Backend – workspace + sections** (versioning, reorder) + tests.
6. **Backend – export PDF** + test.
7. **Frontend – types, services API, stores, mapping d'erreurs.**
8. **Frontend – liste + création + rejoindre.**
9. **Frontend – layout du groupe + vue d'ensemble + membres.**
10. **Frontend – fichiers + TP.**
11. **Frontend – workspace + conflits + export PDF.**
12. **Tests front, polish responsive/accessibilité, mise à jour du `README.md` principal** (ajouter les routes `/app/groupes/*` et la feature dans « MVP »).

> Après chaque étape : lancer les tests (`pytest` / `npm run test`) et vérifier `npm run check` (TypeScript).

---

## 15. 🏁 Critères d'acceptation (Definition of Done)

- [ ] Un étudiant ne voit **que** les groupes de sa classe ; l'accès par ID à un autre groupe renvoie 404.
- [ ] Créer un groupe fait du créateur le chef, sans action supplémentaire.
- [ ] Rejoindre est impossible quand le groupe est plein, même en cas de requêtes simultanées.
- [ ] Le chef peut retirer un membre, transférer le leadership et supprimer le groupe ; un membre ne le peut pas.
- [ ] Le sujet du TP (PDF/photo) peut être importé, remplacé et consulté par les membres uniquement.
- [ ] Les fichiers du groupe sont uploadables, téléchargeables et supprimables selon la matrice de permissions ; aucune URL `/media/` publique.
- [ ] Les sections du workspace s'éditent et se sauvegardent ; un conflit de version est détecté et géré dans l'UI.
- [ ] L'export PDF est généré, correctement nommé, et le contenu est assaini.
- [ ] Toute l'UI est en français, responsive mobile, avec états chargement/vide/erreur.
- [ ] Tests backend et frontend passent ; `npm run check` sans erreur ; aucune utilisation de `any`.
- [ ] Le `README.md` principal est mis à jour.

---

## 16. 🔮 Hors MVP / évolutions

- Collaboration temps réel sur le workspace (WebSocket / CRDT)
- Intégration des photos/figures dans le PDF final
- Invitations par lien ou code, demandes d'adhésion validées par le chef
- Brancher le chat existant sur chaque groupe (un fil de discussion par groupe, accessible aux membres uniquement)
- Notifications (nouveau membre, section modifiée, échéance du TP)
- Espace professeur : dépôt direct du TP, notation, commentaires
- Historique de versions et restauration du document
- Stockage cloud S3-compatible pour les fichiers