from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from .models import SportGroup
from .serializers import SportGroupSerializer
from authentication.models import User
from rest_framework.decorators import action


class SportGroupViewSet(ModelViewSet):
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    serializer_class = SportGroupSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if User.Group.ADMINISTRATOR in user or User.Group.MODERATOR in user:
                return SportGroup.objects.all()
            elif User.Group.TRAINER in user:
                return user.my_groups
            elif user.Group.STUDENT in user:
                return user.sport_groups
        return User.objects.none()

    @action(detail=True, methods=['put'])
    def add_member(self, request, *args, **kwargs):
        try:
            user = User.objects.get(pk=request.data['pk'])
        except:
            return Response({
                'status': False,
                'details': 'No such user'
            }, status=status.HTTP_400_BAD_REQUEST)
        instance = self.get_object()
        instance.members.add(user)
        instance.save()
        serializer = SportGroupSerializer(instance=instance)
        return Response(serializer.data)
