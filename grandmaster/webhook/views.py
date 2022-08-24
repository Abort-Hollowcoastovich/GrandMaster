import logging
from urllib.parse import parse_qs, unquote

from django.core.exceptions import BadRequest
from rest_framework.decorators import api_view
from rest_framework.response import Response

from authentication.models import User
from webhook.utils import UserBuilder

logger = logging.getLogger(__name__)


@api_view(['GET', 'POST'])
def webhook(request):
    try:
        s = request.body.decode('utf8')
        params = parse_qs(unquote(s))
        event = params['event'][0]
        _id = params['data[FIELDS][ID]'][0]
    except Exception:
        raise BadRequest
    if event == 'ONCRMCONTACTUPDATE':
        try:
            user = User.objects.get(b24_id=_id)
            mock_user = UserBuilder(_id).build_user()
            map_user(user, mock_user)
        except User.DoesNotExist as e:
            logger.error(f"can't find user for bitrix id at webhook update: error: {e}")
            return Response(status=400, data={f'no such user'})
        return Response(status=200)
    else:
        logger.info(f'not bitrix update event: event:{event}, id:{_id}')
    return Response(status=200)


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

    user.father_full_name = mock_user.father_full_name
    user.father_birth_date = mock_user.father_birth_date
    user.father_phone_number = mock_user.father_phone_number
    user.father_email = mock_user.father_email

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
