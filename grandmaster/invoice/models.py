from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_init
from django.dispatch import receiver
from django.utils import timezone
from sequences import get_next_value

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
    class Services(models.TextChoices):
        YOOKASSA = 'yookassa'

    service = models.CharField(max_length=256, default=Services.YOOKASSA, choices=Services.choices)
    pay_account = models.ForeignKey(to=PayAccount, on_delete=models.SET_NULL, null=True)
    purpose = models.CharField(max_length=256)
    amount = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    activated_at = models.DateTimeField()
    _must_be_paid_at = models.DateTimeField()
    is_periodic = models.BooleanField()
    period = models.DurationField(null=True, blank=True, validators=[validate_min])

    @property
    def must_be_paid_at(self):
        if self.is_periodic:
            return (timezone.now() - ((timezone.now() - self.activated_at) % self.period)) + (self._must_be_paid_at -
                                                                                              self.activated_at)
        else:
            return self._must_be_paid_at

    def __str__(self):
        return f'{self.service} {self.purpose}'


class UserBill(models.Model):
    yookassa_id = models.CharField(max_length=256, null=True, blank=True)  # 23d93cac-000f-5000-8000-126628f15141
    user = models.ForeignKey(to=User, related_name='bills', on_delete=models.SET_NULL, null=True)
    bill = models.ForeignKey(to=Bill, related_name='bill_users', on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)
    paid = models.BooleanField(default=False)
    paid_at = models.DateTimeField(null=True, blank=True)
    user_bill_number = models.IntegerField(null=True, blank=True)
    pay_account_bill_number = models.IntegerField(null=True, blank=True)

    @property
    def is_blocked(self):
        if self.bill.is_periodic:
            if self.paid_at is None:
                last_payment_date = (timezone.now() - ((timezone.now() - self.bill.activated_at) % self.bill.period))
                return last_payment_date > self.bill.activated_at
            return self.paid_at < ((timezone.now() - ((timezone.now() - self.bill.activated_at) % self.bill.period)) -
                                   self.bill.period)
        else:
            return timezone.now() > self.bill.must_be_paid_at

    @property
    def is_paid(self):
        if self.bill.is_periodic:
            last_payment_date = (timezone.now() - ((timezone.now() - self.bill.activated_at) % self.bill.period))
            next_payment_date = self.bill.must_be_paid_at
            if self.paid_at is None:
                return False
            return last_payment_date < self.paid_at < next_payment_date
        else:
            return self.paid

    # Счет № 2/5-526
    # Где 2 - это порядковый номер счета этого Спортсмена,
    # 5 - порядковый номер Юрлица,
    # 526 - порядковый номер счета у этого Юрлица
    # Описание счета (платежа) будет выглядеть так:
    # Ежегодный взнос. Счет № 2/5-526
    # Где,  "Ежегодный взнос" - это Назначение платежа.
    def __str__(self):
        return f'{self.bill.purpose}. Счет № {self.user_bill_number}/{self.bill.pay_account.id}-' \
               f'{self.pay_account_bill_number}'


@receiver(post_init, sender=UserBill)
def post_init_handler(sender, instance, **kwargs):
    try:
        if instance.user_bill_number is None:
            instance.user_bill_number = get_next_value(f"user_id_{instance.user.id}")
        if instance.pay_account_bill_number is None:
            instance.pay_account_bill_number = get_next_value(f"pay_account_id_{instance.bill.pay_account.id}")
    except Exception:
        pass
