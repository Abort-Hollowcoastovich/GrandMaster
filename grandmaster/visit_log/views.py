from rest_framework.decorators import action
from rest_framework import status
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from authentication.models import User
from sport_groups.models import SportGroup
from schedule.models import Schedule
from .models import VisitLog
from .serializers import VisitLogSerializer


class VisitLogViewSet(ModelViewSet):
    # permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    serializer_class = VisitLogSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if User.Group.ADMINISTRATOR in user or User.Group.MODERATOR in user:
                return VisitLog.objects.all()
            elif User.Group.TRAINER in user:
                return user.my_visit_log
        return VisitLog.objects.none()

    @action(detail=True, methods=['put'])
    def add_member(self, request, *args, **kwargs):
        try:
            group = VisitLog.objects.get(pk=request.data['pk'])
        except User.DoesNotExist:
            return Response({
                'status': False,
                'details': 'No such user'
            }, status=status.HTTP_404_NOT_FOUND)
        instance = self.get_object()
        instance.group.add(group)
        instance.save()
        serializer = VisitLogSerializer(instance=instance)
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
        serializer = VisitLogSerializer(instance=instance)
        return Response(serializer.data)
