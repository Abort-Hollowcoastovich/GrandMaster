from .common import (
    DEBUG,
    env,
)
from yookassa import Configuration

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
    },
    "Moderator": {
        "news": ["add", "delete", "change"],
        "video": ["add", "delete", "change"],
        "instruction": ["add", "delete", "change"],
        "sport group": ["add", "delete", "change"],
        "schedule": ["add", "delete", "change"],
        "gym": ["add", "delete", "change"],
        "event": ["add", "delete", "change"],
    },
    "Trainer": {
        "sport group": ["add", "delete", "change"],
        "schedule": ["add", "delete", "change"],
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

Configuration.account_id = env.str("YOOKASSA_ACCOUNT_ID")
Configuration.secret_key = env.str("YOOKASSA_SECRET_KEY")
