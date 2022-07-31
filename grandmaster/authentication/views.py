import datetime

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .utils import send_sms_code, generate_code
from .models import PhoneOTP

MAX_SEND_TIMES = 10
SECONDS_DELAY_BETWEEN_REQUESTS = 50


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
                elif datetime.datetime.now() - last.last_modified.replace(tzinfo=None) < datetime.timedelta(seconds=SECONDS_DELAY_BETWEEN_REQUESTS):
                    return Response({
                        'status': False,
                        'details': 'Wait 50 seconds to reqest new code'
                    }, status=status.HTTP_429_TOO_MANY_REQUESTS)
                else:
                    last.count += 1
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
