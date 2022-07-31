import random
import requests


def generate_code(length=5):
    return ''.join(str(random.choice(range(0, 10))) for _ in range(length))


def send_sms_code(phone_number: str, code: str):
    requests.get('https://sms.ru/sms/send?api_id=FD33BB41-4A34-F593-9D1F-EFA5663C82BB&to=' + phone_number +
                 '&msg=' + code + '&json=1')
