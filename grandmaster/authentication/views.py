import datetime
from django.utils import timezone

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import PhoneOTP, User
from .utils import send_sms_code, generate_code, is_exists_on_bitrix, get_user_from_bitrix_by_phone, \
    get_trainer_from_bitrix
from grandmaster.settings.project import (
    MAX_SEND_TIMES,
    SECONDS_DELAY_BETWEEN_REQUESTS_TO_LOCK,
    SECONDS_DELAY_BETWEEN_REQUESTS_TO_INCREMENT,
    OTP_EXPIRATION_SECONDS
)


class ValidatePhoneSendOTP(APIView):
    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number')
        if phone_number:
            phone_otp = PhoneOTP.objects.filter(phone_number=phone_number)
            code = generate_code()
            if phone_otp.exists():
                last = phone_otp.first()
                if last.count > MAX_SEND_TIMES:
                    return Response({
                        'status': False,
                        'details': 'Code send request limit exceeded, contact customer support.'
                    }, status=status.HTTP_423_LOCKED)
                elif timezone.now() - last.last_modified < datetime.timedelta(
                        seconds=SECONDS_DELAY_BETWEEN_REQUESTS_TO_LOCK):
                    return Response({
                        'status': False,
                        'details': f'Wait {SECONDS_DELAY_BETWEEN_REQUESTS_TO_LOCK} seconds to request new code'
                    }, status=status.HTTP_429_TOO_MANY_REQUESTS)
                else:
                    if timezone.now() - last.last_modified < datetime.timedelta(
                            seconds=SECONDS_DELAY_BETWEEN_REQUESTS_TO_INCREMENT):
                        last.count += 1
                    last.used = False
                    last.otp = code
                    last.save()
                    send_sms_code(phone_number, code)
                    return Response({
                        'status': True,
                        'details': 'Successfully sent code'
                    }, status=status.HTTP_200_OK)
            else:
                if is_exists_on_bitrix(phone_number):
                    PhoneOTP.objects.create(
                        phone_number=phone_number,
                        otp=code
                    )
                    send_sms_code(phone_number, code)
                    return Response({
                        'status': True,
                        'details': 'Successfully sent code'
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        'status': True,
                        'details': 'Such number does not exists'
                    }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                'status': False,
                'details': 'Phone number is not given in request'
            }, status=status.HTTP_400_BAD_REQUEST)


# request {'phone_number': str, 'code': str}
# response {'access': str, 'refresh': str}
class ValidateOTP(APIView):
    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number')
        otp = request.data.get('code')
        if phone_number and otp:
            phone_otp = PhoneOTP.objects.filter(phone_number=phone_number)
            if phone_otp.exists():
                phone_otp = phone_otp.first()
                print(phone_otp.is_used)
                if not phone_otp.is_used:
                    if otp == phone_otp.otp:
                        if timezone.now() - phone_otp.last_modified < datetime.timedelta(
                                seconds=OTP_EXPIRATION_SECONDS):
                            phone_otp.used = True
                            phone_otp.save()
                            user = User.objects.filter(phone_number=phone_number)
                            if user.exists():
                                user = user.first()
                            else:
                                user = create_user(phone_number)
                            refresh = RefreshToken.for_user(user)
                            return Response({
                                'access': str(refresh.access_token),
                                'refresh': str(refresh),
                            }, status=status.HTTP_200_OK)
                        else:
                            return Response({
                                'status': False,
                                'details': 'Your code has expired'
                            }, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response({
                            'status': False,
                            'details': 'Wrong code'
                        }, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({
                        'status': False,
                        'details': 'You can not use same otp more then once, get new code and try again'
                    }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    'status': False,
                    'details': 'You must validate phone and send code first'
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                'status': False,
                'details': 'You must specify phone number and code'
            }, status=status.HTTP_400_BAD_REQUEST)


def find_trainer(trainer_name: str):
    trainer = User.objects.filter(trainer_name=trainer_name, contact_type=User.CONTACT.TRAINER)
    if trainer.exists():
        return trainer[0]
    trainer = get_trainer_from_bitrix(trainer_name)
    return trainer


def create_user(phone_number: str):
    user = get_user_from_bitrix_by_phone(phone_number)
    user_type = user.contact_type
    if user_type == User.CONTACT.SPORTSMAN:
        user.trainer = find_trainer(user.trainer_name)
        if user.trainer is not None:
            user.trainer.add_group(User.Group.TRAINER)
        user.save()
        user.add_group(User.Group.STUDENT)
        if user.father_phone_number:
            father = User.objects.filter(phone_number=user.father_phone_number)
            if not father.exists():
                father_full_name = user.father_full_name.split()
                last_name = father_full_name[0] if len(father_full_name) >= 1 else ""
                first_name = father_full_name[1] if len(father_full_name) >= 2 else ""
                middle_name = father_full_name[2] if len(father_full_name) >= 3 else ""
                father = User.objects.create_user(
                    phone_number=user.father_phone_number,
                    last_name=last_name,
                    first_name=first_name,
                    middle_name=middle_name,
                    birth_date=user.father_birth_date,
                    contact_type=User.CONTACT.PARENT
                )
                father.add_group(User.Group.PARENT)
            user.parents.add(father)
            user.save()
            father_otp, _ = PhoneOTP.objects.get_or_create(phone_number=user.father_phone_number)
        if user.mother_phone_number:
            mother = User.objects.filter(phone_number=user.mother_phone_number)
            if not mother.exists():
                mother_full_name = user.mother_full_name.split()
                last_name = mother_full_name[0] if len(mother_full_name) >= 1 else ""
                first_name = mother_full_name[1] if len(mother_full_name) >= 2 else ""
                middle_name = mother_full_name[2] if len(mother_full_name) >= 3 else ""
                mother = User.objects.create_user(
                    phone_number=user.mother_phone_number,
                    last_name=last_name,
                    first_name=first_name,
                    middle_name=middle_name,
                    birth_date=user.mother_birth_date,
                    contact_type=User.CONTACT.PARENT
                )
                mother.add_group(User.Group.PARENT)
            user.parents.add(mother)
            user.save()
            mother_otp, _ = PhoneOTP.objects.get_or_create(phone_number=user.mother_phone_number)
    elif user_type == User.CONTACT.TRAINER:
        user.add_group(User.Group.TRAINER)
        pass
    return user
