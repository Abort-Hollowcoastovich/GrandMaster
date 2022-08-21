from __future__ import annotations
import cgi
import requests
import json
import io

from django.core.files import File
from django.core.files.images import ImageFile


def update_tokens():
    client_id = 'local.62e6e40b908a47.85492763'
    client_secret = 'JKv2PnZVQvhimOL0vHAC312zfB7qWVrtFwPowCrKOYxl28Iu4r'
    url = 'https://oauth.bitrix.info/oauth/token/'
    with open('tokens.json', mode='r', encoding='utf8') as file:
        tokens = json.load(file)
        refresh_token = tokens['refresh_token']
    response = requests.get(url=url, params={
        'grant_type': 'refresh_token',
        'client_id': client_id,
        'client_secret': client_secret,
        'refresh_token': refresh_token
    }).json()
    with open('tokens.json', mode='w', encoding='utf8') as file:
        json.dump(response, file, indent=4)


def get_photo(url: str, *args) -> File | None:
    with open('tokens.json', mode='r', encoding='utf8') as file:
        tokens = json.load(file)
        access_token = tokens['access_token']
    response = requests.get(url, params={'auth': access_token})
    if 'image' not in response.headers['Content-Type'] and 'application/pdf' not in response.headers['Content-Type']:
        update_tokens()
        get_photo(url)
        return
    value, params = cgi.parse_header(response.headers['Content-Disposition'])
    return File(io.BytesIO(response.content), name=params['filename'])
