import cgi
import io
import json
import logging
from dataclasses import dataclass
from datetime import datetime

import requests
from bitrix24 import Bitrix24
from django.core.files import File

from authentication.admin import User as UserModel
from grandmaster.settings import (
    CLIENT_ID,
    CLIENT_SECRET,
    REFRESH_TOKEN_URL,
    TOKENS_FILEPATH,
    BITRIX_DOMAIN,
    MAX_TOKEN_REFRESH_TIMES,
)

logger = logging.getLogger(__name__)


@dataclass
class User:
    b24_id: str
    photo: File
    gender: str
    first_name: str
    last_name: str
    middle_name: str
    birth_date: datetime
    contact_type: str
    phone_number: str

    sport_school: str
    department: str
    trainer_name: str
    training_place: str
    tech_qualification: str
    sport_qualification: str
    weight: int
    height: int

    region: str
    city: str
    address: str
    school: str
    med_certificate_date: datetime
    insurance_policy_date: datetime

    father_full_name: str
    father_birth_date: datetime
    father_phone_number: str
    father_email: str

    mother_full_name: str
    mother_birth_date: datetime
    mother_phone_number: str
    mother_email: str

    passport_or_birth_certificate: File
    oms_policy: File
    school_ref: File
    insurance_policy: File
    tech_qual_diplo: File
    med_certificate: File
    foreign_passport: File
    inn: File
    diploma: File
    snils: File


class UserBuilder:
    def __init__(self, b24_id):
        self.b24_id = b24_id
        self.bitrix_user = None
        self.contact_fields = None
        self.access_token = None

    def build_user(self) -> User:
        try:
            self._get_bitrix_user()
        except UserModel.DoesNotExist:
            return None
        self._get_contact_fields()
        self._get_access_token()

        b24_id = self.b24_id
        photo = self._load_file(self.bitrix_user['PHOTO'])
        gender = self.bitrix_user['HONORIFIC']
        first_name = self.bitrix_user['NAME']
        last_name = self.bitrix_user['LAST_NAME']
        middle_name = self.bitrix_user['SECOND_NAME']
        birth_date = self.format_date(self.bitrix_user['BIRTHDATE'])
        contact_type = self.bitrix_user['TYPE_ID']
        phone_number = self.bitrix_user['UF_CRM_1603290188']

        sport_school = self._get_field_value('UF_CRM_1602237440')
        department = self._get_field_value('UF_CRM_1602237201')
        trainer_name = self._get_field_value('UF_CRM_1568455087434')
        training_place = self._get_field_value('UF_CRM_1602445018')
        tech_qualification = self._get_field_value('UF_CRM_1602237683')
        sport_qualification = self._get_field_value('UF_CRM_1602237575')
        weight = self.bitrix_user['UF_CRM_1602237818']
        height = self.bitrix_user['UF_CRM_1602237890']

        region = self._get_field_value('UF_CRM_1628160591')
        city = self.bitrix_user['UF_CRM_1602233637']
        address = self.bitrix_user['UF_CRM_1602233739']
        school = self.bitrix_user['UF_CRM_1602234869']
        med_certificate_date = self.format_date(self.bitrix_user['UF_CRM_1602237971'])
        insurance_policy_date = self.format_date(self.bitrix_user['UF_CRM_1602238043'])

        father_full_name = self.bitrix_user['UF_CRM_1602238578']
        father_birth_date = self.format_date(self.bitrix_user['UF_CRM_1602241365'])
        father_phone_number = self.bitrix_user['UF_CRM_1602241669']
        father_email = self.bitrix_user['UF_CRM_1602241730']

        mother_full_name = self.bitrix_user['UF_CRM_1602241765']
        mother_birth_date = self.format_date(self.bitrix_user['UF_CRM_1602241804'])
        mother_phone_number = self.bitrix_user['UF_CRM_1602241833']
        mother_email = self.bitrix_user['UF_CRM_1602241870']

        passport_or_birth_certificate = self._load_file(self.bitrix_user['UF_CRM_1602238184'])
        oms_policy = self._load_file(self.bitrix_user['UF_CRM_1602238239'])
        school_ref = self._load_file(self.bitrix_user['UF_CRM_1602238293'])
        insurance_policy = self._load_file(self.bitrix_user['UF_CRM_1602238335'])
        tech_qual_diplo = self._load_file(self.bitrix_user['UF_CRM_1602238381'])
        med_certificate = self._load_file(self.bitrix_user['UF_CRM_1602238435'])
        foreign_passport = self._load_file(self.bitrix_user['UF_CRM_1602238474'])
        inn = self._load_file(self.bitrix_user['UF_CRM_CONTACT_1656319970203'])
        diploma = self._load_file(self.bitrix_user['UF_CRM_CONTACT_1656319776732'])
        if isinstance(self.bitrix_user['UF_CRM_CONTACT_1656320071632'], list) and len(
                self.bitrix_user['UF_CRM_CONTACT_1656320071632']) > 0:
            snils = self._load_file(self.bitrix_user['UF_CRM_CONTACT_1656320071632'][0])
        else:
            snils = self._load_file(self.bitrix_user['UF_CRM_CONTACT_1656320071632'])
        return User(
            b24_id=b24_id,
            photo=photo,
            gender=gender,
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name,
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
            passport_or_birth_certificate=passport_or_birth_certificate,
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

    def _get_bitrix_user(self):
        b = Bitrix24('gm61.bitrix24.ru', user_id=2261)
        method = 'crm.contact.list'
        params = {
            'select': ['*', 'UF_*', 'PHONE', 'EMAIL', 'IM'],
            'filter': {'ID': self.b24_id},
        }
        raw_result = b.call_webhook(method, '6ot3rs39vklb84zs', params)
        try:
            self.bitrix_user = raw_result['result'][0]
        except Exception as e:
            logger.error(f"get_bitrix_user: error: {str(e)} result: {raw_result}")
            raise UserModel.DoesNotExist

    def _get_contact_fields(self):  # TODO: const
        url = 'https://gm61.bitrix24.ru/rest/2261/6ot3rs39vklb84zs/crm.contact.fields.json'
        self.contact_fields = requests.get(url).json()['result']

    def _get_field_value(self, field_title):
        item_id = self.bitrix_user[field_title]
        for field, value in self.contact_fields.items():
            if field == field_title:
                items = value['items']
                for item in items:
                    if item['ID'] == item_id:
                        return item['VALUE']
        return None

    def format_date(self, string_date):
        if string_date is not None and string_date:
            return datetime.fromisoformat(string_date).replace(tzinfo=None)
        return None

    def _get_access_token(self):
        with open(TOKENS_FILEPATH, mode='r', encoding='utf8') as file:
            tokens = json.load(file)
            self.access_token = tokens['access_token']

    def _update_tokens(self):
        with open(TOKENS_FILEPATH, mode='r', encoding='utf8') as file:
            tokens = json.load(file)
            refresh_token = tokens['refresh_token']
        response = requests.get(url=REFRESH_TOKEN_URL, params={
            'grant_type': 'refresh_token',
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'refresh_token': refresh_token
        }).json()
        self.access_token = response['access_token']
        with open(TOKENS_FILEPATH, mode='w', encoding='utf8') as file:
            json.dump(response, file, indent=4)

    def _load_file(self, urls: dict, times=1) -> File:
        if times > MAX_TOKEN_REFRESH_TIMES:
            return None
        try:
            if urls is not None and urls:
                url = BITRIX_DOMAIN + urls['downloadUrl']
                response = requests.get(url, params={'auth': self.access_token})
                if 'image' not in response.headers['Content-Type'] and 'application/pdf' not in response.headers['Content-Type']:
                    self._update_tokens()
                    return self._load_file(urls, times + 1)
                value, params = cgi.parse_header(response.headers['Content-Disposition'])
                return File(io.BytesIO(response.content), name=params['filename'])
        except Exception as e:
            logger.error(f"file download error: {str(e)}")
        return None


def map_user(user, mock_user):
    user.b24_id = mock_user.b24_id
    user.photo = mock_user.photo
    user.gender = mock_user.gender
    user.first_name = mock_user.first_name
    user.last_name = mock_user.last_name
    user.middle_name = mock_user.middle_name
    user.birth_date = mock_user.birth_date
    user.contact_type = mock_user.contact_type
    user.phone_number = mock_user.phone_number
    # TODO: change gym and trainer
    user.sport_school = mock_user.sport_school
    user.department = mock_user.department
    user.trainer_name = mock_user.trainer_name
    user.training_place = mock_user.training_place
    user.tech_qualification = mock_user.tech_qualification
    user.sport_qualification = mock_user.sport_qualification
    user.weight = mock_user.weight
    user.height = mock_user.height

    user.region = mock_user.region
    user.city = mock_user.city
    user.address = mock_user.address
    user.school = mock_user.school
    user.med_certificate_date = mock_user.med_certificate_date
    user.insurance_policy_date = mock_user.insurance_policy_date
    # TODO: change father
    user.father_full_name = mock_user.father_full_name
    user.father_birth_date = mock_user.father_birth_date
    user.father_phone_number = mock_user.father_phone_number
    user.father_email = mock_user.father_email
    # TODO: change mother
    user.mother_full_name = mock_user.mother_full_name
    user.mother_birth_date = mock_user.mother_birth_date
    user.mother_phone_number = mock_user.mother_phone_number
    user.mother_email = mock_user.mother_email

    user.passport_or_birth_certificate = mock_user.passport_or_birth_certificate
    user.oms_policy = mock_user.oms_policy
    user.school_ref = mock_user.school_ref
    user.insurance_policy = mock_user.insurance_policy
    user.tech_qual_diplo = mock_user.tech_qual_diplo
    user.med_certificate = mock_user.med_certificate
    user.foreign_passport = mock_user.foreign_passport
    user.inn = mock_user.inn
    user.diploma = mock_user.diploma
    user.snils = mock_user.snils
    user.save()
