# serializers.py
from rest_framework import serializers
from .models import Graduation


class GraduationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Graduation
        fields = ['id', 'name']
