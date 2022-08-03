import datetime

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import PhoneOTP, User
from .utils import send_sms_code, generate_code

MAX_SEND_TIMES = 10
SECONDS_DELAY_BETWEEN_REQUESTS_TO_LOCK = 50
SECONDS_DELAY_BETWEEN_REQUESTS_TO_INCREMENT = 600
OTP_EXPIRATION_SECONDS = 300


class ValidatePhoneSendOTP(APIView):
    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number')
        if phone_number:
            # TODO: проверка на наличие телефона в битриксе
            phone = str(phone_number)
            phone_otp = PhoneOTP.objects.filter(phone__iexact=phone)
            code = generate_code()
            if phone_otp.exists():
                last = phone_otp.first()
                if last.count > MAX_SEND_TIMES:
                    return Response({
                        'status': False,
                        'details': 'Code send request limit exceeded, contact customer support.'
                    }, status=status.HTTP_423_LOCKED)
                elif datetime.datetime.now() - last.last_modified.replace(tzinfo=None) < datetime.timedelta(seconds=SECONDS_DELAY_BETWEEN_REQUESTS_TO_LOCK):
                    return Response({
                        'status': False,
                        'details': f'Wait {SECONDS_DELAY_BETWEEN_REQUESTS_TO_LOCK} seconds to reqest new code'
                    }, status=status.HTTP_429_TOO_MANY_REQUESTS)
                else:
                    if datetime.datetime.now() - last.last_modified.replace(tzinfo=None) < datetime.timedelta(seconds=SECONDS_DELAY_BETWEEN_REQUESTS_TO_INCREMENT):
                        last.count += 1
                    last.used = False
                    last.otp = code
                    last.save()
                    send_sms_code(phone, code)
                    return Response({
                        'status': True,
                        'details': 'Successfully sended code'
                    }, status=status.HTTP_200_OK)
            else:
                PhoneOTP.objects.create(
                    phone=phone,
                    otp=code
                )
                send_sms_code(phone, code)
                return Response({
                    'status': True,
                    'details': 'Successfully sended code'
                }, status=status.HTTP_200_OK)
        else:
            return Response({
                'status': False,
                'details': 'Phone number is not given in request'
            }, status=status.HTTP_400_BAD_REQUEST)


# request {'phone_number': int, 'code': int}
# response {'refresh': str, 'access': str}
class ValidateOTP(APIView):
    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number')
        otp = request.data.get('code')
        if phone_number and otp:
            phone_number = str(phone_number)
            otp = str(otp)
            phone_otp = PhoneOTP.objects.filter(phone=phone_number)
            if phone_otp.exists():
                phone_otp = phone_otp.first()
                if not phone_otp.is_used:
                    if otp == phone_otp.otp:
                        if datetime.datetime.now() - phone_otp.last_modified.replace(tzinfo=None) < datetime.timedelta(seconds=OTP_EXPIRATION_SECONDS):
                            phone_otp.used = True
                            phone_otp.save()
                            user = User.objects.filter(phone=phone_number)
                            if user.exists():
                                user = user.first()
                            else:
                                # TODO: Получить имя пользователя и роль из битрикса

                                user = User.objects.create_user(phone=phone_number, full_name='Abobov Aboba Abobovich')

                            refresh = RefreshToken.for_user(user)
                            return Response({
                                'refresh': str(refresh),
                                'access': str(refresh.access_token)
                            }, status=status.HTTP_200_OK)
                        else:
                            return Response({
                                'status': False,
                                'details': 'Your otp has expired'
                            }, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response({
                            'status': False,
                            'details': 'Wrong otp'
                        }, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({
                        'status': False,
                        'details': 'You can not use same otp more then once, get new otp and try again'
                    }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    'status': False,
                    'details': 'You must validate phone and send otp first'
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                'status': False,
                'details': 'You must specify phone number and otp'
            }, status=status.HTTP_400_BAD_REQUEST)