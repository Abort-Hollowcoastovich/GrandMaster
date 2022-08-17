import json

from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET', 'POST'])
def webhook(request):
    print(request.method)
    print(request.body.decode('utf8'))
    return Response({'detail': 'hello'})
