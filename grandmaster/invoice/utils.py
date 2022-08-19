import uuid

from yookassa import Payment


def create_payment(amount: int, description: str):
    return Payment.create({
        "amount": {
            "value": str(amount),
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "https://app.grandmaster.club/"
        },
        "capture": True,
        "description": description
    }, uuid.uuid4())
