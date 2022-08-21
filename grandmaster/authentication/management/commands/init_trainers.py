from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    help = "Creates users"

    def handle(self, *args, **options):
        # fetch_users()
        create_users()


def create_users():
    print('starting creating users')
    import requests
    import json
    def send_code(phone_number):
        result = requests.post('https://app.grandmaster.center/auth/send_code/', {
            'phone_number': phone_number,
        })
        print(result.text)

    def validate_code(phone_number):
        result = requests.post('https://app.grandmaster.center/auth/validate_code/', {
            'phone_number': phone_number,
            'code': '12345'
        })
        print(result.text)

    with open('result.json', 'r', encoding='utf-8') as file:
        result = json.load(file)
        for person in result:
            user_type = person['TYPE_ID']
            if user_type == 'PARTNER':
                phone_number = person['UF_CRM_1603290188']
                if phone_number is not None:
                    print(f'creating trainer {phone_number}')
                    send_code(phone_number)
                    validate_code(phone_number)


def fetch_users():
    from fast_bitrix24 import Bitrix
    import json

    b24 = Bitrix('https://gm61.bitrix24.ru/rest/2261/6ot3rs39vklb84zs/')

    params = {
        'select': ['*', 'UF_*', 'PHONE', 'EMAIL', 'IM'],
    }

    with open('result.json', 'w', encoding='utf-8') as f:
        json.dump(b24.get_all(method='crm.contact.list', params=params), f, indent=4, ensure_ascii=False)
    print('users fetched')
