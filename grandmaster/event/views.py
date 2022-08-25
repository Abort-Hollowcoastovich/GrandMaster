# from rest_framework.pagination import PageNumberPagination
from django.core.exceptions import BadRequest
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView

from authentication.models import User
from .models import Event
from .serializers import EventSerializer


# class StandardResultsSetPagination(PageNumberPagination):
#     page_size = 10
#     page_size_query_param = 'page_size'
#     max_page_size = 1000


class EventViewSet(ModelViewSet):
    permission_classes = [DjangoModelPermissions]
    # pagination_class = StandardResultsSetPagination
    serializer_class = EventSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if User.Group.ADMINISTRATOR in user or User.Group.MODERATOR in user:
                return Event.objects.all()
        return Event.objects.filter(hidden=False)


class EventMembersView(APIView):
    def get_valid_members(self):
        user = self.request.user
        if user.is_anonymous:
            members = User.objects.none()
        elif User.Group.TRAINER in user:
            members = user.students.all()
        elif User.Group.PARENT in user:
            members = user.children.all()
        elif User.Group.MODERATOR in user or User.Group.ADMINISTRATOR in user:
            members = User.objects.all()
        else:
            members = User.objects.filter(id=user.id)
        return [member.id for member in members]

    def validate_members(self):
        members = self.request.data.get('members', None)
        if members is None:
            raise BadRequest
        valid_members = self.get_valid_members()
        for member in members:
            if member not in valid_members:
                raise ValidationError("You can't add not your user")
        return members

    def get_event(self) -> Event:
        params = self.request.query_params
        event_id = params.get('event', None)
        if event_id is None:
            raise BadRequest
        if type(event_id) is not int:
            if type(event_id) is not str:
                raise ValidationError
            else:
                if not event_id.isdigit():
                    raise ValidationError
                else:
                    event_id = int(event_id)
        event = Event.objects.filter(id=event_id)
        if not event.exists():
            raise NotFound
        return event[0]

    def put(self, request: Request):
        event = self.get_event()
        members_to_add = self.validate_members()
        valid_members = self.get_valid_members()
        members_to_remove = list(set(valid_members) - set(members_to_add))
        for member in members_to_remove:
            event.members.remove(member)
        event.members.add(*members_to_add)
        event.save()
        return Response(EventSerializer(event, context={'request': request}).data, status=200)
