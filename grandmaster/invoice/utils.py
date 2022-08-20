import uuid

from yookassa import Payment, Configuration

from invoice.models import PayAccount


def create_payment(amount: int, description: str, pay_account: PayAccount):
    Configuration.configure(pay_account.account_id, pay_account.secret_key)
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
