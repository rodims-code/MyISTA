from django.db.models import QuerySet
from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import (
    UserSerializer, BatimentSerializer, SalleSerializer,
    AffectationSalleSerializer, InfosEssentiellesSerializer, DocumentSerializer,
    ActivityLogSerializer,  FeedbackSerializer
)
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import User, Batiment, Salle, AffectationSalle, InfosEssentielles, Document, ActivityLog, Filiere, feedback


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def patch(self, request):
        serializer = UserSerializer(
            request.user, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


class BatimentListCreate(generics.ListCreateAPIView):
    queryset = Batiment.objects.all()
    serializer_class = BatimentSerializer
    permission_classes = [AllowAny]


class BatimentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Batiment.objects.all()
    serializer_class = BatimentSerializer
    permission_classes = [AllowAny]


class SalleListCreate(generics.ListCreateAPIView):
    queryset = Salle.objects.all()
    serializer_class = SalleSerializer
    permission_classes = [AllowAny]


class SalleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Salle.objects.all()
    serializer_class = SalleSerializer
    permission_classes = [AllowAny]


class AffectationSalleListCreate(generics.ListCreateAPIView):
    queryset = AffectationSalle.objects.all()
    serializer_class = AffectationSalleSerializer
    permission_classes = [IsAuthenticated]


class AffectationSalleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = AffectationSalle.objects.all()
    serializer_class = AffectationSalleSerializer
    permission_classes = [IsAuthenticated]


class InfosEssentiellesListCreate(generics.ListCreateAPIView):
    queryset = InfosEssentielles.objects.all()
    serializer_class = InfosEssentiellesSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        statut = "approuve" if self.request.user.role == "admin" else "en_attente"
        instance = serializer.save(statut=statut)
        ActivityLog.objects.create(
            user=self.request.user,
            action="create",
            cible_type="InfosEssentielles",
            cible_nom=instance.titre
        )


class InfosEssentiellesDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = InfosEssentielles.objects.all()
    serializer_class = InfosEssentiellesSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        original = self.get_object()
        instance = serializer.save()
        if original.statut == "en_attente" and instance.statut == "approuve":
            ActivityLog.objects.create(
                user=self.request.user,
                action="approve",
                cible_type="InfosEssentielles",
                cible_nom=instance.titre
            )


class DocumentListCreate(generics.ListCreateAPIView):
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if self.request.user.role == "admin" :
            return Document.objects.all()
        else :
            return Document.objects.filter(
                niveau__nom=user.niveau,
                filiere__nom=user.filiere
            )

    def perform_create(self, serializer):
        statut = "approuve" if self.request.user.role == "admin" else "en_attente"
        instance = serializer.save(uploader=self.request.user, statut=statut)
        ActivityLog.objects.create(
            user=self.request.user,
            action="create",
            cible_type="Document",
            cible_nom=instance.titre
        )


class DocumentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        original = self.get_object()
        instance = serializer.save()
        if original.statut == "en_attente" and instance.statut == "approuve":
            ActivityLog.objects.create(
                user=self.request.user,
                action="approve",
                cible_type="Document",
                cible_nom=instance.titre
            )

class DashboardStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        stats = {
            "etudiants": User.objects.filter(role="student").count(),
            "filieres": Filiere.objects.count(),
            "salles": Salle.objects.count(),
            "documents": Document.objects.filter(statut="approuve").count(),
        }
        recent_activities = ActivityLog.objects.order_by("-date_action")[:5]
        activities_data = ActivityLogSerializer(recent_activities, many=True).data
        return Response({
            "stats": stats,
            "recent_activity": activities_data
        })

class UserRoleUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        if request.user.role != "admin":
            return Response({"error": "Accès refusé"}, status=403)
        try:
            user_to_update = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"error": "Utilisateur introuvable"}, status=404)
        
        new_role = request.data.get("role")
        if new_role not in dict(User.ROLE_CHOICES).keys():
            return Response({"error": "Rôle invalide"}, status=400)
            
        user_to_update.role = new_role
        user_to_update.save()
        
        ActivityLog.objects.create(
            user=request.user,
            action="role_change",
            cible_type="User",
            cible_nom=user_to_update.username,
            details=f"Nouveau rôle: {new_role}"
        )
        return Response({"message": "Rôle mis à jour"})

class UserListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = User.objects.all()
        roles = self.request.query_params.get('role', None)
        if roles:
            role_list = roles.split(',')
            queryset = queryset.filter(role__in=role_list)
        return queryset
    
class FeedbackListCreate(generics.ListCreateAPIView):
    queryset = feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)