from rest_framework import generics
from .models import Level
from .serializers import LevelSerializer


class LevelView(generics.CreateAPIView, generics.ListAPIView):
    queryset = Level.objects.all()
    serializer_class = LevelSerializer

