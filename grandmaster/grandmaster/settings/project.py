from .common import (
    DEBUG,
    env,
)

# Custom settings

GROUPS = {
    "Administrator": {
        "news": ["add", "delete", "change"],
        "video": ["add", "delete", "change"],
        "instruction": ["add", "delete", "change"],
        "sport group": ["add", "delete", "change"],
        "schedule": ["add", "delete", "change"],
        "gym": ["add", "delete", "change"],
        "event": ["add", "delete", "change"],
        "content": ["add", "delete", "change"],
        "visit_log": ["add", "delete", "change"],
    },
    "Moderator": {
        "news": ["add", "delete", "change"],
        "video": ["add", "delete", "change"],
        "instruction": ["add", "delete", "change"],
        "sport group": ["add", "delete", "change"],
        "schedule": ["add", "delete", "change"],
        "gym": ["add", "delete", "change"],
        "event": ["add", "delete", "change"],
        "content": ["add", "delete", "change"],
        "visit log": ["add", "delete", "change"],
    },
    "Trainer": {
        "sport group": ["add", "delete", "change"],
        "schedule": ["add", "delete", "change"],
        "visit log": ["add", "delete", "change"],
    },
    "Student": {
    },
    "Parent": {
    },
}

# AUTH
MAX_SEND_TIMES = env.int("MAX_SEND_TIMES")
SECONDS_DELAY_BETWEEN_REQUESTS_TO_LOCK = env.int("SECONDS_DELAY_BETWEEN_REQUESTS_TO_LOCK")
SECONDS_DELAY_BETWEEN_REQUESTS_TO_INCREMENT = env.int("SECONDS_DELAY_BETWEEN_REQUESTS_TO_INCREMENT")
OTP_EXPIRATION_SECONDS = env.int("OTP_EXPIRATION_SECONDS")

# BITRIX:
# WEBHOOK_URL
CLIENT_ID = env.str('CLIENT_ID')
CLIENT_SECRET = env.str('CLIENT_SECRET')

REFRESH_TOKEN_URL = 'https://oauth.bitrix.info/oauth/token/'
TOKENS_FILEPATH = 'tokens.json'
BITRIX_DOMAIN = 'https://gm61.bitrix24.ru'
MAX_TOKEN_REFRESH_TIMES = 10
