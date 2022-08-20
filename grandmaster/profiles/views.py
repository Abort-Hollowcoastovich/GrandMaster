from rest_framework import generics
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model

from .serializers import UserDetailsSerializer, DocumentsDetailsSerializer, UserListSerializer
from .permissions import IsOwnerOrTrainerOrAdminOrModerOnlyPermissions

User = get_user_model()


class UserDetails(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailsSerializer
    permission_classes = [IsAuthenticated]


class SelfDetails(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return Response(UserDetailsSerializer(request.user, context={'request': request}).data)


class DocumentsDetails(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = DocumentsDetailsSerializer
    permission_classes = [IsAuthenticated and IsOwnerOrTrainerOrAdminOrModerOnlyPermissions]


class UserList(generics.ListAPIView):
    def list(self, request, *args, **kwargs):
        user = self.request.user
        if user.is_anonymous:
            return Response({
                'status': False,
                'details': 'Unauthorized'
            },
                status=status.HTTP_401_UNAUTHORIZED)
        users = [user]
        for child in user.children.all():
            users.append(child)
        return Response(UserListSerializer(users, many=True, context={'request': request}).data)
