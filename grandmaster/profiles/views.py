from rest_framework import generics
from rest_framework.permissions import DjangoModelPermissions, BasePermission
from rest_framework.response import Response

from authentication.models import User
from .models import UserProfile, Documents
from .serializers import UserProfileSerializer, UserProfileHyperlinkSerializer, DocumentsSerializer


class ProfileDetails(generics.RetrieveAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [DjangoModelPermissions]


class ProfileList(generics.ListAPIView):
    def list(self, request, *args, **kwargs):
        profiles = []
        user = self.request.user
        if hasattr(user, 'profile'):
            profiles.append(user.profile)
        for child in user.children.all():
            if hasattr(child, 'profile'):
                profiles.append(child.profile)
        return Response(UserProfileHyperlinkSerializer(profiles, many=True, context={'request': request}).data)


class IsOwnerOnlyPermissions(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (obj.user_profile.user == request.user) or \
               (User.Group.ADMINISTRATOR in request.user) or \
               (User.Group.MODERATOR in request.user)


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


class DocumentsDetails(generics.RetrieveAPIView):
    queryset = Documents.objects.all()
    serializer_class = DocumentsSerializer
    # Can get docs owner OR administrator/moderator
    # permission_classes = [IsOwnerOnlyPermissions | DjangoModelPermissionsWithRead]
    permission_classes = [IsOwnerOnlyPermissions]
