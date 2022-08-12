import requests

from django.core.management import BaseCommand

from gyms.models import Gym


class Command(BaseCommand):
    help = "Fetches gyms from bitrix"

    def handle(self, *args, **options):
        url = 'https://gm61.bitrix24.ru/rest/2261/6ot3rs39vklb84zs/crm.contact.fields.json'
        result = requests.get(url).json()['result']
        for el in result['UF_CRM_1602445018']["items"]:
            Gym.objects.create(
                b24_id=el['ID'],
                address=el['VALUE']
            )
