from rest_framework import generics

from .serializers import GymSerializer
from .models import Gym


class GymListView(generics.ListAPIView):
    queryset = Gym.objects.all()
    serializer_class = GymSerializer
