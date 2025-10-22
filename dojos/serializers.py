# serializers.py
from rest_framework import serializers
from .models import Dojo

class DojoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dojo
        fields = ['id', 'tradename']