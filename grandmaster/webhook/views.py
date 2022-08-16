import json

from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET', 'POST'])
def webhook(request):
    print(request.method)
    print(json.loads(request.body))
    return Response({'detail': 'hello'})
