from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.viewsets import ModelViewSet

from authentication.models import User
from .models import Event
from .serializers import EventSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000


class EventViewSet(ModelViewSet):
    permission_classes = [DjangoModelPermissions]
    pagination_class = StandardResultsSetPagination
    serializer_class = EventSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if User.Group.ADMINISTRATOR in user or User.Group.MODERATOR in user:
                return Event.objects.all()
        return Event.objects.filter(hidden=False)
