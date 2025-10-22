from rest_framework import serializers
from django.contrib.auth.models import User
from django.db import transaction, IntegrityError
from karatecas.models import Karateca


class KaratecaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Karateca
        fields = '__all__'


class PublicKaratekaRegisterSerializer(serializers.ModelSerializer):
    """
    Serializer público para cadastro de Karatecas.
    Cria o usuário Django vinculado automaticamente.
    """
    password = serializers.CharField(write_only=True, required=True, min_length=6)

    class Meta:
        model = Karateca
        fields = [
            'name', 'cpf', 'email', 'celphone',
            'genre', 'graduation', 'dan',
            'active', 'dojo', 'monthlypay',
            'password'
        ]
        extra_kwargs = {
            'active': {'read_only': True},
            'dojo': {'required': True},
            'monthlypay': {'required': True},
            'genre': {'required': True},
        }

    def validate_email(self, value):
        """Impede duplicidade de e-mails no sistema."""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este e-mail já está sendo usado.")
        return value

    @transaction.atomic
    def create(self, validated_data):
        """
        Cria o Karateca e o usuário Django de forma atômica.
        Se algum passo falhar, tudo é revertido.
        """
        password = validated_data.pop('password')
        email = validated_data.get('email')
        name = validated_data.get('name')

        try:
            # 🔹 Cria usuário
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=name
            )

            # 🔹 Cria karateca vinculado
            karateka = Karateca.objects.create(
                user=user,
                active='ATIVO',
                **validated_data
            )

            return karateka

        except IntegrityError as e:
            raise serializers.ValidationError({
                "detail": f"Erro de integridade ao salvar o Karateca: {str(e)}"
            })
