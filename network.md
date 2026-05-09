# 📱 MyISTA — Social Network Architecture & Roadmap

## 🎯 Vision

Créer une plateforme **sociale + académique** inspirée d'Instagram, où les étudiants peuvent :

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

---

# 🌐 NETWORK APP (une seule app ⭐)

Structure :

```
network/
├── models.py          # All models
├── views.py           # All viewsets
├── serializers.py     # All serializers
├── urls.py            # Routing
├── permissions.py     # Custom permissions
├── services/
│   └── recommendation.py  # Algorithm logic
└── tests/
```

---

## 📸 MODELS

### ➕ Follow

```python
class Follow(models.Model):
    follower = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('follower', 'following')
```

### Post

```python
class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    image = models.ImageField(upload_to='posts/', null=True, blank=True)
    file = models.FileField(upload_to='posts/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### Comment

```python
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### Like

```python
class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'post')
```

### Conversation (Messaging)

```python
class Conversation(models.Model):
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### Message

```python
class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    file = models.FileField(upload_to='messages/', null=True, blank=True)
    seen = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
```

### Notification

```python
class Notification(models.Model):
    TYPES = [
        ('like', 'Like'),
        ('comment', 'Comment'),
        ('follow', 'Follow'),
        ('message', 'Message'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    type = models.CharField(max_length=20, choices=TYPES)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
```

---

# 🧠 ALGORITHME (service dans network)

Créer un service :

```
network/services/recommendation.py
```

## Logique simple (MVP)

* posts récents
* boost si :
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

* créer app network
* implémenter feed
* ajouter follow
* models Post, Comment, Like, Follow

## MOYEN TERME

* messaging (Conversation, Message)
* notifications (Notification)

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

# 🧠 RÈGLE D'OR

👉 Familiarité + utilité = succès

* Design connu → adoption rapide
* Fonction unique → rétention

---

# 🔥 OBJECTIF FINAL

Créer :

> Le réseau social étudiant n°1 en Afrique

---
