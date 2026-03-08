from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, matricule, username, password=None, **extra_fields):
        if not matricule:
            raise ValueError('The Matricule must be set')
        user = self.model(matricule=matricule, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, matricule, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(matricule, username, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    matricule = models.CharField(max_length=100, unique=True)
    username = models.CharField(max_length=100)
    niveau = models.CharField(max_length=100)
    filiere = models.CharField(max_length=100)
    role = models.CharField(max_length=100, default='student')
    date_inscription = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'matricule'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

class Batiment(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nom

class Salle(models.Model):
    nom = models.CharField(max_length=100)
    batiment = models.ForeignKey(Batiment, on_delete=models.CASCADE)

    def __str__(self):
        return self.nom

class AffectationSalle(models.Model):
    niveau = models.CharField(max_length=100)
    filiere = models.CharField(max_length=100)
    salle = models.ForeignKey(Salle, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.niveau} - {self.filiere}"

class InfosEssentielles(models.Model):
    titre = models.CharField(max_length=100)
    contenu = models.TextField()
    categorie = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titre

class Document(models.Model):
    titre = models.CharField(max_length=100)
    fichier_url = models.CharField(max_length=200)  # URL or file path
    niveau = models.CharField(max_length=100)
    filiere = models.CharField(max_length=100)
    cours = models.CharField(max_length=100)
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)
    date_upload = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titre