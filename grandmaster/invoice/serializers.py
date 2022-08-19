from rest_framework import serializers
from .models import PayAccount, UserBill, Bill


class PayAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayAccount
        fields = '__all__'
        read_only_fields = ['id']


class BillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = [
            'service',
            'purpose',
            'amount',
            'activated_at',
            # "_must_be_paid_at",
            'must_be_paid_at',
            "is_periodic",
            "period",
        ]


class UserBillSerializer(serializers.ModelSerializer):
    bill = BillSerializer()

    class Meta:
        model = UserBill
        fields = [
            'id',
            'user',
            'bill',
            'is_active',
            'is_paid',
            'is_blocked'
        ]
