from django.db.models import QuerySet
from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from .serializers import (
    UserSerializer, BatimentSerializer, SalleSerializer,
    AffectationSalleSerializer, InfosEssentiellesSerializer, DocumentSerializer,
    ActivityLogSerializer,  FeedbackSerializer, EventSerializer
)
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import User, Batiment, Salle, AffectationSalle, InfosEssentielles, Document, ActivityLog, Filiere, feedback, Event


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

class ToggleFavoriteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            document = Document.objects.get(pk=pk)
        except Document.DoesNotExist:
            return Response({"error": "Document introuvable"}, status=404)

        user = request.user
        if document in user.favoris.all():
            user.favoris.remove(document)
            action = "removed"
        else:
            user.favoris.add(document)
            action = "added"
        
        return Response({"status": action, "favoris": [doc.id for doc in user.favoris.all()]})

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
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            serializer.save(user=None)

class FeedbackDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticated]

class FeedbackReplyView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        if request.user.role == "student":
            return Response({"error": "Accès refusé"}, status=403)
        try:
            fb = feedback.objects.get(pk=pk)
        except feedback.DoesNotExist:
            return Response({"error": "Feedback introuvable"}, status=404)
        
        reponse_text = request.data.get("reponse")
        if not reponse_text:
            return Response({"error": "La réponse est obligatoire"}, status=400)
            
        fb.reponse = reponse_text
        fb.save()
        
        return Response({"message": "Réponse envoyée avec succès"})

class EventListCreate(generics.ListCreateAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == "admin":
            return Event.objects.all()
            
        from django.db.models import Q
        return Event.objects.filter(
            Q(filiere__nom=user.filiere, niveau__nom=user.niveau) |
            Q(filiere__isnull=True) | Q(niveau__isnull=True)
        )

    def create(self, request, *args, **kwargs):
        if request.user.role != "admin":
            raise PermissionDenied("Seul l'admin peut créer des événements.")
            
        data = request.data.copy()
        repetition = data.pop('repetition', 'none')
        fin_repetition_str = data.pop('fin_repetition', None)
        
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        base_event = serializer.save(createur=request.user)
        
        created_events = [base_event]
        
        if repetition != 'none' and fin_repetition_str:
            from datetime import datetime, timedelta
            try:
                fin_repetition = datetime.strptime(fin_repetition_str, '%Y-%m-%d').date()
                current_start = base_event.debut
                current_end = base_event.fin
                
                while True:
                    if repetition == 'quotidienne':
                        current_start += timedelta(days=1)
                        current_end += timedelta(days=1)
                    elif repetition == 'hebdomadaire':
                        current_start += timedelta(weeks=1)
                        current_end += timedelta(weeks=1)
                    elif repetition == 'mensuelle':
                        # Simple 4-week jump if dateutil is unavailable
                        current_start += timedelta(weeks=4)
                        current_end += timedelta(weeks=4)
                    else:
                        break
                        
                    if current_start.date() > fin_repetition:
                        break
                        
                    new_event = Event.objects.create(
                        titre=base_event.titre,
                        description=base_event.description,
                        debut=current_start,
                        fin=current_end,
                        all_day=base_event.all_day,
                        salle=base_event.salle,
                        filiere=base_event.filiere,
                        niveau=base_event.niveau,
                        createur=request.user
                    )
                    created_events.append(new_event)
            except Exception as e:
                print("Recurrence error:", e)

        ActivityLog.objects.create(
            user=request.user,
            action="create",
            cible_type="Event",
            cible_nom=base_event.titre + (" (Répétition)" if len(created_events) > 1 else "")
        )
        
        return Response(self.get_serializer(created_events, many=True).data, status=201)

class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        if self.request.user.role != "admin":
            raise PermissionDenied("Seul l'admin peut modifier des événements.")
        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user.role != "admin":
            raise PermissionDenied("Seul l'admin peut supprimer des événements.")
        instance.delete()
