import json

from django.core.management import BaseCommand

from authentication.models import User
from webhook.utils import UserBuilder, create_user


class Command(BaseCommand):
    help = "Creates users"

    def handle(self, *args, **options):
        # fetch_users()

        with open('result.json', 'r', encoding='utf-8') as file:
            result = json.load(file)
            for person in result:
                id_ = person['ID']
                if not User.objects.filter(b24_id=id_).exists():
                    try:
                        mock_user = UserBuilder(id_).build_user()
                        create_user(mock_user)
                        print(f'created: {person["UF_CRM_1603290188"]} - {person["SECOND_NAME"]} {person["NAME"]} {person["LAST_NAME"]}')
                    except Exception as e:
                        print(f'ERROR {e} - {person["SECOND_NAME"]} {person["NAME"]} {person["LAST_NAME"]}')


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
