from rest_framework import serializers
from .models import PayAccount


class PayAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayAccount
        fields = '__all__'
        read_only_fields = ['pk']
