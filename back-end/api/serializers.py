from rest_framework import serializers
from .models import User, Batiment, Salle, AffectationSalle, InfosEssentielles, Document, ActivityLog, Filiere, Niveau, feedback
from django.contrib.auth import get_user_model


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id',"matricule", "username", "password", "niveau", "filiere", "role", "date_inscription"]
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
    filiere = serializers.SlugRelatedField(
        queryset=Filiere.objects.all(),
        slug_field='nom'
    )
    niveau = serializers.SlugRelatedField(
        queryset=Niveau.objects.all(),
        slug_field='nom'
    )

    class Meta:
        model = Document
        fields = '__all__'
        read_only_fields = ['uploader', 'statut']


class ActivityLogSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = ActivityLog
        fields = '__all__'

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = feedback
        fields = '__all__'