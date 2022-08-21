from django.test import TestCase
from rest_framework.test import APIRequestFactory
from .views import ScheduleViewSet
from .models import Schedule
from sport_groups.models import SportGroup
from authentication.models import User

class ScheduleTest(TestCase):
    def setUp(self):
        User.objects.create(first_name='Seva', group=TRAINER)
    factory = APIRequestFactory()
    request = factory.get('/schedule/', format='json')
    view = ScheduleViewSet.as_view({'get': 'list'})


