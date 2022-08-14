from rest_framework import generics
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model

from .serializers import UserDetailsSerializer, DocumentsDetailsSerializer, UserListSerializer

User = get_user_model()


class UserDetails(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailsSerializer
    permission_classes = [DjangoModelPermissions]  # TODO: уточнить права


class SelfDetails(generics.RetrieveAPIView):
    def get(self, request, *args, **kwargs):
        return Response(UserDetailsSerializer(request.user, context={'request': request}).data)


class DocumentsDetails(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = DocumentsDetailsSerializer
    permission_classes = [DjangoModelPermissions]  # TODO: уточнить права


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


# class IsOwnerOrAdminOrModerOnlyPermissions(BasePermission):
#     def has_object_permission(self, request, view, obj):
#         return (obj.user_profile.user == request.user) or \
#                (User.Group.ADMINISTRATOR in request.user) or \
#                (User.Group.MODERATOR in request.user)

# class DjangoModelPermissionsWithRead(DjangoModelPermissions):
#     perms_map = {
#         'GET': ['%(app_label)s.view_%(model_name)s'],
#         'OPTIONS': [],
#         'HEAD': [],
#         'POST': ['%(app_label)s.add_%(model_name)s'],
#         'PUT': ['%(app_label)s.change_%(model_name)s'],
#         'PATCH': ['%(app_label)s.change_%(model_name)s'],
#         'DELETE': ['%(app_label)s.delete_%(model_name)s'],
#     }
