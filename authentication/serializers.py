# jiyuu/authentication/serializers.py
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'username'

    def validate(self, attrs):
        
        credentials = {
            'username': attrs.get('username'),
            'password': attrs.get('password')
        }
        #print("login recebido: ", attrs)
        # Se for email, busca o usuário
        if '@' in credentials['username']:
            try:
                user = User.objects.get(email=credentials['username'])
                credentials['username'] = user.username
            except User.DoesNotExist:
                pass

        return super().validate(credentials)