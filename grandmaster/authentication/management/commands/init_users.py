# from django.core.management import BaseCommand
# from django.contrib.auth.models import Group, Permission
# from django.contrib.auth import get_user_model
# import logging
#
# User = get_user_model()
#
# USERS = {
#     "student_1": ["80000000010", "Abobov Aboba Abobovich", User.Role.STUDENT],
#     "student_2": ["80000000010", "Abobov Aboba Abobovich", User.Role.STUDENT],
# }
#
#
# class Command(BaseCommand):
#     help = "Creates users"
#
#     def handle(self, *args, **options):
#         for phone_number, full_name, role in USERS:
#             new_user, created = User.objects.get_or_create(phone=phone_number, full_name=full_name, role=role)
#
#             new_user.save()
