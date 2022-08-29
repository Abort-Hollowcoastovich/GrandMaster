import logging
from urllib.parse import parse_qs, unquote

from django.core.exceptions import BadRequest
from rest_framework.decorators import api_view
from rest_framework.response import Response

from authentication.models import User
from webhook.utils import UserBuilder, map_user

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
    elif event == 'ONCRMCONTACTCREATE':
        logger.info(f'user created id:{_id}')
    else:
        logger.info(f'not bitrix update event: event:{event}, id:{_id}')
    return Response(status=200)
