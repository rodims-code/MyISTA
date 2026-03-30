# create_superuser.py
import os
import sys
import django

# Définir les settings Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Lire les variables d'environnement
username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
email = os.environ.get("DJANGO_SUPERUSER_EMAIL")
password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

# Vérifier que toutes les variables sont définies
if not all([username, email, password]):
    print("❌ Erreur : Une ou plusieurs variables d'environnement pour le superuser ne sont pas définies.")
    print("Veuillez définir DJANGO_SUPERUSER_USERNAME, DJANGO_SUPERUSER_EMAIL et DJANGO_SUPERUSER_PASSWORD.")
    sys.exit(1)

# Créer le superuser si nécessaire
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"✅ Superuser '{username}' créé avec succès !")
else:
    print(f"ℹ️ Superuser '{username}' existe déjà.")