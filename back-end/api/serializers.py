from rest_framework import serializers
from .models import User, Batiment, Salle, AffectationSalle, InfosEssentielles, Document
from django.contrib.auth import get_user_model


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["matricule", "username", "password", "niveau", "filiere", "role", "date_inscription"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class BatimentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batiment
        fields = '__all__'


class SalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Salle
        fields = '__all__'


class AffectationSalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = AffectationSalle
        fields = '__all__'


class InfosEssentiellesSerializer(serializers.ModelSerializer):
    class Meta:
        model = InfosEssentielles
        fields = '__all__'


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'