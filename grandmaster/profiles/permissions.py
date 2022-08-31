from django.contrib.auth import get_user_model
from rest_framework.permissions import BasePermission

User = get_user_model()


class IsOwnerOrTrainerOrAdminOrModerOnlyPermissions(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_anonymous:
            return False
        if request.user.children.all().exists() and obj in request.user.children.all():
            return True
        return ((obj == request.user) or
                (User.Group.ADMINISTRATOR in request.user) or
                (User.Group.TRAINER in request.user) or
                (User.Group.MODERATOR in request.user))
