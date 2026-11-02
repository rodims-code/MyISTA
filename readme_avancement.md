export const projectReadme = `
# MyISTA — Point d'avancement

> Dernière mise à jour : 2 novembre 2026

MyISTA est une plateforme web destinée aux étudiants de l'ISTA. Le projet combine les services académiques essentiels avec une expérience sociale inspirée des réseaux modernes.

## Vision

Centraliser dans une seule application :

- les informations et documents académiques ;
- les salles, affectations et événements du campus ;
- le profil et les favoris des étudiants ;
- les publications, commentaires et interactions sociales ;
- la messagerie et les notifications.

## État actuel

### Frontend — SvelteKit

Le frontend est déjà structuré autour de SvelteKit, TypeScript, Tailwind CSS, daisyUI et Lucide Svelte. Il comprend :

- une landing page et les écrans de connexion/inscription ;
- un dashboard protégé avec navigation globale ;
- les pages d'accueil, profil, carte, salles, affectations, documents, informations et feedbacks ;
- les favoris, notifications et messages ;
- les composants sociaux de publication, création de post et commentaires ;
- un thème et une interface responsive orientée mobile ;
- des services API dédiés pour l'utilisateur et le réseau.

### Backend — Django

Le backend utilise Django, Django REST Framework, PostgreSQL prévu pour la production et une authentification JWT. Deux domaines fonctionnels sont présents :

- `api` : utilisateurs, rôles, filières, niveaux, bâtiments, salles, affectations, documents, informations essentielles, événements, feedbacks et journal d'activité ;
- `network` : abonnements, publications, commentaires, likes, favoris, conversations, messages et notifications.

Les migrations Django existent pour les fonctionnalités académiques et la phase sociale. Le modèle utilisateur prévoit les rôles étudiant, délégué et administrateur.

## Fonctionnalités déjà disponibles

- Authentification et routes protégées ;
- dashboard étudiant ;
- consultation des salles et affectations ;
- documents académiques avec filtres métier ;
- informations essentielles ;
- favoris ;
- calendrier d'événements ;
- feedbacks ;
- profils ;
- publications avec image ou fichier ;
- commentaires, likes et abonnements ;
- conversations, messages et notifications.

## Architecture du dépôt

```text
MyISTA/
├── cors/                  # Backend Django
│   ├── api/               # Fonctionnalités académiques et comptes
│   ├── network/           # Fonctionnalités sociales
│   └── backend/           # Configuration Django
├── web/                   # Frontend SvelteKit
│   ├── src/routes/        # Pages publiques et dashboard
│   ├── src/lib/           # API, composants et utilitaires
│   └── static/            # Fichiers statiques
├── network.md             # Architecture et roadmap détaillées
└── readme.ts             # Ce point d'avancement exploitable en TypeScript
```

## Démarrage local

### Frontend

```bash
cd web
npm install
npm run dev
```

### Backend

```bash
cd cors
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Niveau de maturité

Le socle MVP académique est en place et la phase sociale est déjà intégrée au code et aux migrations. Le projet est donc au stade de prototype fonctionnel avancé : il peut continuer à évoluer vers une première version utilisable par des étudiants, mais nécessite encore une validation complète des parcours, des tests et du déploiement.

## Prochaines priorités

1. Vérifier tous les parcours frontend/backend avec un environnement propre ;
2. compléter les tests API, composants et authentification ;
3. renforcer les permissions, la validation des fichiers et la gestion des erreurs ;
4. préparer le déploiement et la configuration PostgreSQL ;
5. transformer le frontend en PWA avec manifest, icônes, service worker et mode d'installation mobile ;
6. ajouter ensuite le temps réel pour la messagerie et les notifications ;
7. développer progressivement les recommandations, groupes et suggestions d'utilisateurs.

## Positionnement produit

MyISTA ne doit pas être un simple clone d'Instagram. Sa valeur vient de l'association suivante :

> Une interface sociale familière + des services académiques utiles au quotidien.

L'objectif à long terme est de devenir un réseau social étudiant adapté aux réalités des établissements africains.
`;

export default projectReadme;
