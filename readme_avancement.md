# MyISTA — mise à jour

## Changements réalisés

- Messages et Notifications sont maintenant accessibles depuis la barre supérieure, avec des boutons compacts.
- La sidebar est allégée : les deux liens ont été retirés de la liste principale.
- Le modèle utilisateur possède maintenant une photo de profil (`photo_profil`) stockée dans `profiles/`.
- La page Paramètres permet de choisir et d'enregistrer une image de profil.
- L'avatar est affiché avec une initiale de secours dans la navbar, le profil, les publications, les commentaires et la messagerie.
- Les sérialiseurs Django exposent la photo pour l'utilisateur courant et les utilisateurs du réseau.

## Fichiers principaux

- `cors/api/models.py` et `cors/api/migrations/0012_user_photo_profil.py` : champ photo utilisateur.
- `cors/api/serializers.py` et `cors/network/serializers.py` : exposition de la photo via l'API.
- `web/src/routes/dashboard/+layout.svelte` : navbar et sidebar.
- `web/src/routes/dashboard/settings/+page.svelte` : upload et aperçu du profil.
- `web/src/lib/components/network/` : avatars des publications et commentaires.
- `web/src/routes/dashboard/messages/+page.svelte` : avatars des conversations.

## À vérifier

Après récupération des changements, appliquer les migrations avec `python manage.py migrate` depuis `cors`, puis tester l'upload d'une image et son affichage sur plusieurs écrans.
