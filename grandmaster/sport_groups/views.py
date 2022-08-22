from rest_framework.decorators import action
from rest_framework import status
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics

from authentication.models import User
from .models import SportGroup
from .serializers import SportGroupSerializer, SportsmenSerializer
from .permissions import IsTrainerOrAdminOrModerOnlyPermissions


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
    def fetch_members(self, request, *args, **kwargs):
        members_list = request.data
        if type(members_list) != list:
            pass  # TODO: raise
        instance = self.get_object()
        for member_id in members_list:
            if member_id not in instance.members.all():
                try:
                    member = User.objects.get(id=member_id)
                    instance.members.add(member)
                except User.DoesNotExist:
                    return Response({
                        'status': False,
                        'details': 'No such user'
                    }, status=status.HTTP_404_NOT_FOUND)
        for member in instance.members.all():
            if member.id not in members_list:
                instance.members.remove(member)
        serializer = SportGroupSerializer(instance=instance)
        return Response(serializer.data)


class SportsmenList(generics.ListAPIView):
    queryset = User.objects.filter().all()  # TODO: filter
    serializer_class = SportsmenSerializer
    permission_classes = [IsTrainerOrAdminOrModerOnlyPermissions]

