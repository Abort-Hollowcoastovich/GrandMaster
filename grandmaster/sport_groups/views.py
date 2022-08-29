from rest_framework import generics, status
from rest_framework.decorators import action
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from authentication.models import User
from .models import SportGroup
from .permissions import IsTrainerOrAdminOrModerOnlyPermissions
from .serializers import SportGroupSerializer, SportsmenSerializer, TrainerSerializer


class SportGroupViewSet(ModelViewSet):
    permission_classes = [DjangoModelPermissions]
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
        return SportGroup.objects.none()

    @action(detail=True, methods=['patch'])
    def remove_member(self, request, *args, **kwargs):
        try:
            user = User.objects.get(pk=request.data['id'])
        except User.DoesNotExist:
            return Response({
                'status': False,
                'details': 'No such user'
            }, status=status.HTTP_404_NOT_FOUND)
        except KeyError:
            return Response({
                'status': False,
                'details': 'Must specify user id in body'
            }, status=status.HTTP_400_BAD_REQUEST)
        instance = self.get_object()
        instance.members.remove(user)
        instance.save()
        serializer = SportGroupSerializer(instance=instance)
        return Response(serializer.data)


class SportsmenList(generics.ListAPIView):
    serializer_class = SportsmenSerializer
    permission_classes = [IsTrainerOrAdminOrModerOnlyPermissions]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if User.Group.ADMINISTRATOR in user or User.Group.MODERATOR in user:
                return User.objects.all().order_by('last_name', 'first_name', 'middle_name')
            elif User.Group.TRAINER in user:
                return User.objects.filter(trainer=user).order_by('last_name', 'first_name', 'middle_name')
        return SportGroup.objects.none()


class TrainersList(generics.ListAPIView):
    queryset = User.objects.filter(contact_type=User.CONTACT.TRAINER).all().order_by(
        'last_name', 'first_name', 'middle_name')
    serializer_class = TrainerSerializer
    permission_classes = [IsAuthenticated]
