from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


# -------------------------
# USER MANAGER
# -------------------------

class UserManager(BaseUserManager):
    def create_user(self, matricule, username, password=None, **extra_fields):
        if not matricule:
            raise ValueError("Le matricule est obligatoire")

        user = self.model(
            matricule=matricule,
            username=username,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, matricule, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(matricule, username, password, **extra_fields)


# -------------------------
# FILIERE
# -------------------------

class Filiere(models.Model):
    nom = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nom


# -------------------------
# NIVEAU
# -------------------------

class Niveau(models.Model):
    nom = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nom


# -------------------------
# USER
# -------------------------

class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
    ("student", "Student"),
    ("delegate", "Delegate"),
    ("admin", "Admin"),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="student"
    )

    matricule = models.CharField(max_length=100, unique=True)
    username = models.CharField(max_length=100)

    filiere = models.ForeignKey(
        Filiere,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    niveau = models.ForeignKey(
        Niveau,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    date_inscription = models.DateTimeField(auto_now_add=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = "matricule"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.username


# -------------------------
# BATIMENT
# -------------------------

class Batiment(models.Model):

    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nom


# -------------------------
# SALLE
# -------------------------

class Salle(models.Model):

    nom = models.CharField(max_length=100)

    batiment = models.ForeignKey(
        Batiment,
        on_delete=models.CASCADE,
        related_name="salles"
    )

    def __str__(self):
        return f"{self.nom} ({self.batiment.nom})"


# -------------------------
# AFFECTATION DES SALLES
# -------------------------

class AffectationSalle(models.Model):

    niveau = models.ForeignKey(
        Niveau,
        on_delete=models.CASCADE
    )

    filiere = models.ForeignKey(
        Filiere,
        on_delete=models.CASCADE
    )

    salle = models.ForeignKey(
        Salle,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.niveau} - {self.filiere} → {self.salle}"


# -------------------------
# INFOS ESSENTIELLES
# -------------------------

class InfosEssentielles(models.Model):

    titre = models.CharField(max_length=200)

    contenu = models.TextField()

    categorie = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titre


# -------------------------
# DOCUMENTS
# -------------------------

class Document(models.Model):

    titre = models.CharField(max_length=200)

    fichier = models.FileField(
        upload_to="documents/"
    )

    cours = models.CharField(max_length=100)

    filiere = models.ForeignKey(
        Filiere,
        on_delete=models.CASCADE
    )

    niveau = models.ForeignKey(
        Niveau,
        on_delete=models.CASCADE
    )

    uploader = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    date_upload = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titre