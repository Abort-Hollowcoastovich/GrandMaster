from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

from authentication.models import User


class Command(BaseCommand):
    help = "Link parents"

    def handle(self, *args, **options):
        users = User.objects.filter(contact_type=User.CONTACT.SPORTSMAN)
        for user in users:
            father_number = user.father_phone_number
            mother_number = user.mother_phone_number
            try:
                if father_number:
                    father = User.objects.get(phone_number=father_number)
                    user.parents.add(father)
                    user.save()
                    print(f'added {user} {father}')
            except:
                print('error found father')
            try:
                if mother_number:
                    mother = User.objects.get(phone_number=mother_number)
                    user.parents.add(mother)
                    user.save()
                    print(f'added {user} {mother}')
            except:
                print('error found mother')
