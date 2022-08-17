from rest_framework import serializers
from .models import Instruction


class InstructionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instruction
        fields = '__all__'
