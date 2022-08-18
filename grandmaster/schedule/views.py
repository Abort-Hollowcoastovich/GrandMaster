from rest_framework.decorators import action
from rest_framework import status
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from authentication.models import User
from sport_groups.models import SportGroup
from .models import Schedule
from .serializers import ScheduleSerializer


class ScheduleViewSet(ModelViewSet):
    # permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    serializer_class = ScheduleSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if User.Group.ADMINISTRATOR in user or User.Group.MODERATOR in user:
                return Schedule.objects.all()
            elif User.Group.TRAINER in user:
                return user.my_groups
            elif user.Group.STUDENT in user:
                return user.sport_groups
        return Schedule.objects.none()

    @action(detail=True, methods=['put'])
    def add_member(self, request, *args, **kwargs):
        try:
            group = SportGroup.objects.get(pk=request.data['pk'])
        except User.DoesNotExist:
            return Response({
                'status': False,
                'details': 'No such user'
            }, status=status.HTTP_404_NOT_FOUND)
        instance = self.get_object()
        instance.group.add(group)
        instance.save()
        serializer = ScheduleSerializer(instance=instance)
        return Response(serializer.data)

    @action(detail=True, methods=['put'])
    def remove_member(self, request, *args, **kwargs):
        try:
            group = SportGroup.objects.get(pk=request.data['pk'])
        except User.DoesNotExist:
            return Response({
                'status': False,
                'details': 'No such user'
            }, status=status.HTTP_404_NOT_FOUND)
        instance = self.get_object()
        instance.group.remove(group)
        instance.save()
        serializer = ScheduleSerializer(instance=instance)
        return Response(serializer.data)

