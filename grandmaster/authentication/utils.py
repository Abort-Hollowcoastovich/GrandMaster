import random
import requests
from bitrix24 import Bitrix24
from datetime import datetime

from django.contrib.auth import get_user_model

from utils.photo import get_photo
from authentication.models import Document
from grandmaster.settings.common import DEBUG

User = get_user_model()

webhook = "https://gm61.bitrix24.ru/rest/2261/6ot3rs39vklb84zs/"
domain = 'https://gm61.bitrix24.ru'


def generate_code(length=5):
    if DEBUG:
        return '12345'
    return ''.join(str(random.choice(range(0, 10))) for _ in range(length))


def send_sms_code(phone_number: str, code: str):
    if DEBUG:
        print(phone_number, code)
    else:
        requests.get('https://sms.ru/sms/send?api_id=FD33BB41-4A34-F593-9D1F-EFA5663C82BB&to=' + phone_number +
                     '&msg=' + code + '&json=1')


def is_exists_on_bitrix(phone_number: str):
    b = Bitrix24('gm61.bitrix24.ru', user_id=2261)
    method = 'crm.contact.list'
    params = {
        'select': ['*', 'UF_*', 'PHONE', 'EMAIL', 'IM'],
        'filter': {'UF_CRM_1603290188': phone_number},
    }  # TODO: fix filtering
    result = b.call_webhook(method, '6ot3rs39vklb84zs', params)['result']
    print('len:', len(result))
    return bool(result)


def find_field_by_id(field_name, id):
    url = 'https://gm61.bitrix24.ru/rest/2261/6ot3rs39vklb84zs/crm.contact.fields.json'
    response = requests.get(url).json()['result']
    for item in response[field_name]['items']:
        if item['ID'] == id:
            return item['VALUE']


def get_user_from_bitrix(phone_number: str):
    b = Bitrix24('gm61.bitrix24.ru', user_id=2261)
    method = 'crm.contact.list'
    params = {
        'select': ['*', 'UF_*', 'PHONE', 'EMAIL', 'IM'],
        'filter': {'UF_CRM_1603290188': phone_number},
    }
    result = b.call_webhook(method, '6ot3rs39vklb84zs', params)
    print(result)  # may be QUERY_LIMIT_EXCEEDED error
    result = result['result']
    if not result:
        return
    else:
        result = result[0]

    load = lambda x: None if x is None or not x else get_photo(domain + x['downloadUrl'])
    make_date = lambda x: datetime.fromisoformat(x).replace(tzinfo=None) if x is not None and x else None

    b24_id = result['ID']
    photo = load(result['PHOTO'])
    gender = result['HONORIFIC']
    first_name = result['NAME']
    last_name = result['SECOND_NAME']
    birth_date = make_date(result['BIRTHDATE'])
    contact_type = result['TYPE_ID']
    phone_number = result['UF_CRM_1603290188']

    sport_school = find_field_by_id('UF_CRM_1602237440', result['UF_CRM_1602237440'])
    department = find_field_by_id('UF_CRM_1602237201', result['UF_CRM_1602237201'])
    trainer_name = find_field_by_id('UF_CRM_1568455087434', result['UF_CRM_1568455087434'])
    training_place = find_field_by_id('UF_CRM_1602445018', result['UF_CRM_1602445018'])
    tech_qualification = find_field_by_id('UF_CRM_1602237683', result['UF_CRM_1602237683'])
    sport_qualification = find_field_by_id('UF_CRM_1602237575', result['UF_CRM_1602237575'])
    weight = result['UF_CRM_1602237818']
    height = result['UF_CRM_1602237890']

    region = find_field_by_id('UF_CRM_1628160591', result['UF_CRM_1628160591'])
    city = result['UF_CRM_1602233637']
    address = result['UF_CRM_1602233739']
    school = result['UF_CRM_1602234869']
    med_certificate_date = make_date(result['UF_CRM_1602237971'])
    insurance_policy_date = make_date(result['UF_CRM_1602238043'])

    father_full_name = result['UF_CRM_1602238578']
    father_birth_date = make_date(result['UF_CRM_1602241365'])
    father_phone_number = result['UF_CRM_1602241669']
    father_email = result['UF_CRM_1602241730']

    mother_full_name = result['UF_CRM_1602241765']
    mother_birth_date = make_date(result['UF_CRM_1602241804'])
    mother_phone_number = result['UF_CRM_1602241833']
    mother_email = result['UF_CRM_1602241870']
    oms_policy = load(result['UF_CRM_1602238239'])
    school_ref = load(result['UF_CRM_1602238293'])
    insurance_policy = load(result['UF_CRM_1602238335'])
    tech_qual_diplo = load(result['UF_CRM_1602238381'])
    med_certificate = load(result['UF_CRM_1602238435'])
    foreign_passport = load(result['UF_CRM_1602238474'])
    inn = load(result['UF_CRM_CONTACT_1656319970203'])
    diploma = load(result['UF_CRM_CONTACT_1656319776732'])
    if result['UF_CRM_CONTACT_1656320071632'] is list:
        snils = load(result['UF_CRM_CONTACT_1656320071632'][0])
    else:
        snils = load(result['UF_CRM_CONTACT_1656320071632'][0])
    user = User.objects.create_user(
        b24_id=b24_id,
        photo=photo,
        gender=gender,
        first_name=first_name,
        last_name=last_name,
        birth_date=birth_date,
        contact_type=contact_type,
        phone_number=phone_number,
        sport_school=sport_school,
        department=department,
        trainer_name=trainer_name,
        training_place=training_place,
        tech_qualification=tech_qualification,
        sport_qualification=sport_qualification,
        weight=weight,
        height=height,
        region=region,
        city=city,
        address=address,
        school=school,
        med_certificate_date=med_certificate_date,
        insurance_policy_date=insurance_policy_date,
        father_full_name=father_full_name,
        father_birth_date=father_birth_date,
        father_phone_number=father_phone_number,
        father_email=father_email,
        mother_full_name=mother_full_name,
        mother_birth_date=mother_birth_date,
        mother_phone_number=mother_phone_number,
        mother_email=mother_email,
        oms_policy=oms_policy,
        school_ref=school_ref,
        insurance_policy=insurance_policy,
        tech_qual_diplo=tech_qual_diplo,
        med_certificate=med_certificate,
        foreign_passport=foreign_passport,
        inn=inn,
        diploma=diploma,
        snils=snils,
    )
    [Document.objects.create(user=user, image=load(el, 'other')) for el in result['UF_CRM_CONTACT_1656822613397']]
    return user
