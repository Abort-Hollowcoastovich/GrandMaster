from urllib.parse import parse_qs, unquote

from django.core.exceptions import BadRequest
from rest_framework.decorators import api_view
from rest_framework.response import Response


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
        print('bitrix update', event, id)  # update
    return Response(status=200)
