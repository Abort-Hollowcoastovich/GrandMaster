# from datetime import datetime
# from urllib.parse import parse_qs
#
# import django
# import jwt
#
# from channels.db import database_sync_to_async
# from channels.middleware import BaseMiddleware
# from django.contrib.auth.models import AnonymousUser
# from authentication.models import User
# from django.db import close_old_connections
#
# django.setup()
#
# from grandmaster import settings
#
#
# @database_sync_to_async
# def get_user(token):
#     try:
#         payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.SIMPLE_JWT['ALGORITHM'])
#     except:
#         return AnonymousUser()
#
#     token_exp = datetime.fromtimestamp(payload['exp'])
#     if token_exp < datetime.utcnow():
#         return AnonymousUser()
#
#     try:
#         user = User.objects.get(id=payload['user_id'])
#     except User.DoesNotExist:
#         return AnonymousUser()
#
#     return user
#
#
# class TokenAuthMiddleware(BaseMiddleware):
#
#     async def __call__(self, scope, receive, send):
#         close_old_connections()
#         try:
#             token = parse_qs(scope["query_string"].decode("utf8"))["token"][0]
#         except KeyError:
#             token = None
#         user = await get_user(token)
#         scope['user'] = user
#         return await super().__call__(scope, receive, send)
#
#
# def JwtAuthMiddlewareStack(inner):
#     return TokenAuthMiddleware(inner)
