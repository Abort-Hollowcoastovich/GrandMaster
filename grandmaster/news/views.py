from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import News
from .serializers import NewsSerializer


class Upload(ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
