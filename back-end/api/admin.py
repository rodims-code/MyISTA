from django.contrib import admin
from .models import (
    Filiere,
    Niveau,
    User,
    Batiment,
    Salle,
    AffectationSalle,
    InfosEssentielles,
    Document,
    feedback,
)


# Register your models here.
admin.site.register(Filiere)
admin.site.register(Niveau)
admin.site.register(User)
admin.site.register(Batiment)
admin.site.register(Salle)
admin.site.register(AffectationSalle)
admin.site.register(InfosEssentielles)
admin.site.register(Document)
admin.site.register(feedback)
