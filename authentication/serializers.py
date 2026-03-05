# jiyuu/authentication/serializers.py
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from dojos.models import DojoMembership


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)

        user = self.user

        membership = (
            DojoMembership.objects
            .select_related('dojo')
            .filter(user=user)
            .first()
        )

        data['user'] = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': membership.role if membership else 'STUDENT',
            'dojo_id': membership.dojo.id if membership else None,
            'dojo_name': membership.dojo.tradename if membership else None,
        }

        return data
 