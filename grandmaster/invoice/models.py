from datetime import timedelta

from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

User = get_user_model()


class PayAccount(models.Model):
    name = models.CharField(max_length=256)
    account_id = models.CharField(max_length=256)
    secret_key = models.CharField(max_length=256)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


def validate_min(value: timedelta):
    if value < timedelta(days=30):
        raise ValidationError('Minimum period is month (30 days)')


class Bill(models.Model):
    class Services:
        YOOKASSA = 'yookassa'

    yookassa_id = models.CharField(max_length=256)  # 23d93cac-000f-5000-8000-126628f15141
    service = models.CharField(max_length=256, default=Services.YOOKASSA)
    pay_account = models.ForeignKey(to=PayAccount, on_delete=models.DO_NOTHING)
    payer = models.ForeignKey(to=User, on_delete=models.DO_NOTHING)
    purpose = models.CharField(max_length=256)
    amount = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    activated_at = models.DateTimeField()
    _must_be_paid_at = models.DateTimeField(null=True)
    _paid = models.BooleanField(default=False)  # TODO: Оплачен /Не оплачен (ответ платежного сервиса)
    paid_at = models.DateTimeField()  # TODO: Дата совершения платежа (ответ платежного сервиса)
    is_periodic = models.BooleanField()  # Регулярность - Разовый/Регулярный
    period = models.DurationField(null=True, validators=[validate_min])  # (если регулярный) Периодичность
    is_active = models.BooleanField(default=True)  # не заблокрированный / заблокированный счет

    @property
    def must_be_paid_at(self):
        if self.is_periodic:
            return (self.activated_at - ((timezone.now() - self.activated_at) % self.period)) + self.period
        else:
            return self._must_be_paid_at

    @property
    def is_paid(self) -> bool:
        # dif = (timezone.now() - self.activated_at) % self.period
        # last_must_payment_date = self.activated_at - dif
        # if last_must_payment_date - self.period < self.paid_at < last_must_payment_date:
        #     if self.paid_at > last_must_payment_date:
        #         return self.
        # else:
        #     pass  # Пропущена оплата!
        if self.is_periodic:
            return self.paid_at < self.must_be_paid_at
        else:
            return self._paid
