from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import (
    UserSerializer, BatimentSerializer, SalleSerializer,
    AffectationSalleSerializer, InfosEssentiellesSerializer, DocumentSerializer
)
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import User, Batiment, Salle, AffectationSalle, InfosEssentielles, Document


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
    permission_classes = [IsAuthenticated]


class BatimentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Batiment.objects.all()
    serializer_class = BatimentSerializer
    permission_classes = [IsAuthenticated]


class SalleListCreate(generics.ListCreateAPIView):
    queryset = Salle.objects.all()
    serializer_class = SalleSerializer
    permission_classes = [IsAuthenticated]


class SalleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Salle.objects.all()
    serializer_class = SalleSerializer
    permission_classes = [IsAuthenticated]


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


class InfosEssentiellesDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = InfosEssentielles.objects.all()
    serializer_class = InfosEssentiellesSerializer
    permission_classes = [IsAuthenticated]


class DocumentListCreate(generics.ListCreateAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]


class DocumentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]