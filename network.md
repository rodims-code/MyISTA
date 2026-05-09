# 📱 MyISTA — Social Network Architecture & Roadmap

## 🎯 Vision

Créer une plateforme **sociale + académique** inspirée d’Instagram, où les étudiants peuvent :

* partager du contenu
* échanger
* accéder à des ressources éducatives

👉 Objectif :

> Une expérience familière (Instagram-like) + une valeur unique (documents académiques)

---

# 🧱 STACK TECHNIQUE

## Frontend

* SvelteKit
* Tailwind CSS
* daisyUI

## Backend

* Django
* Django REST Framework
* PostgreSQL
* JWT (auth)

---

# 🏗️ ARCHITECTURE BACKEND

## App principale network

```
# User + logique existante
# réseau social
# chat
# notifications
# fichiers académiques (déjà existant)
```

---

## 👤 User (dans api)

* Custom User
* Favoris
* Rôle (student, admin…)

### ➕ Follow (à ajouter)

```python
class Follow(models.Model):
    follower = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='followers', on_delete=models.CASCADE)
```

---

# 📸 POSTS (app: posts)

## Models

### Post

* author (User)
* content (text)
* image (optionnel)
* fichier (PDF, doc…)
* created_at

### Comment

* post
* author
* content
* created_at

### Like

* user
* post

---

# 💬 MESSAGING (app: messaging)

## Models

### Conversation

* participants (ManyToMany User)
* created_at

### Message

* conversation
* sender
* content
* file (optionnel)
* seen (bool)
* created_at

---

# 🔔 NOTIFICATIONS (app: notifications)

## Model

### Notification

* user (receveur)
* sender
* type (like, comment, follow, message)
* is_read
* created_at

---

# 🧠 ALGORITHME (pas une app ❗)

Créer un service :

```
posts/services/recommendation.py
```

## Logique simple (MVP)

* posts récents
* * boost si :

  - même filière
  - beaucoup de likes
  - interaction fréquente

---

# 🎨 DESIGN SYSTEM (IMPORTANT)

## Inspiration : Instagram

### UI clé :

* Feed scroll infini
* Stories (plus tard)
* Cards modernes
* Boutons minimalistes
* Icônes (lucide-svelte)

---

## 🎯 Expérience utilisateur

### Feed

* posts des abonnements
* tri intelligent
* loading skeleton

### Profil

* photo + bio
* posts grid
* followers / following

### Chat

* bulles modernes
* style Messenger / Instagram DM
* temps réel (WebSocket plus tard)

---

# 🔥 FEATURES MVP

## Phase 1

* Auth
* Profil
* Follow
* Post
* Like
* Comment

---

## Phase 2

* Chat (DM)
* Notifications
* Favoris

---

## Phase 3

* Algorithme
* Groupes
* Suggestions utilisateurs

---

# 📚 FEATURE UNIQUE MYISTA

## Social + Académique

* Poster des documents
* Télécharger des cours
* Filtrer :

  * filière
  * niveau
  * cours

👉 Différence clé :

> Instagram ne fait pas ça.

---

# 🧩 FRONTEND STRUCTURE (Svelte)

```
src/
│
├── lib/
│   ├── components/
│   │   ├── PostCard.svelte
│   │   ├── CommentSection.svelte
│   │   ├── ChatBox.svelte
│   │   └── Navbar.svelte
│
├── routes/
│   ├── feed/
│   ├── profile/
│   ├── messages/
│   └── documents/
```

---

# 🔐 SÉCURITÉ

* JWT auth
* Permissions (DRF)
* Signalement de contenu
* Blocage utilisateur (plus tard)

---

# ⚡ UX MODERNE

* Dark mode 🌙
* Animations
* Responsive mobile 📱
* Feedback visuel (loading, hover)

---

# 🚀 ROADMAP

## COURT TERME

* créer app posts
* implémenter feed
* ajouter follow

## MOYEN TERME

* messaging
* notifications

## LONG TERME

* carte campus interactive
* modèle 3D Blender
* géolocalisation

---

# 💡 STRATÉGIE PRODUIT

Ne fais pas :

> un clone Instagram

Fais :

> Instagram + Université

---

# 🧠 RÈGLE D’OR

👉 Familiarité + utilité = succès

* Design connu → adoption rapide
* Fonction unique → rétention

---

# 🔥 OBJECTIF FINAL

Créer :

> Le réseau social étudiant n°1 en Afrique

---
