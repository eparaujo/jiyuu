from rest_framework import serializers
from django.contrib.auth.models import User
from django.db import transaction, IntegrityError
from karatecas.models import Karateca
from dojos.models import DojoMembership
from dojos.choices import DojoRole
from dashboards.models import Dashboard



class KaratecaSerializer(serializers.ModelSerializer):
    graduation = serializers.StringRelatedField()
    dojo = serializers.StringRelatedField()
    genre = serializers.StringRelatedField()

    class Meta:
        model = Karateca
        fields = '__all__'  


class GraduationStatusSerializer(serializers.Serializer):
    current_graduation = serializers.CharField(allow_null=True)
    next_graduation = serializers.CharField(allow_null=True)
    min_months = serializers.IntegerField()
    elapsed_months = serializers.IntegerField()
    remaining_months = serializers.IntegerField()

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
            'active', 'dojo', 'password'
        ]
        extra_kwargs = {
            'active': {'read_only': True},
            'dojo': {'required': True},
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
        dojo = validated_data.get('dojo')

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

            # 🔴 REGRA DE NEGÓCIO CENTRAL
            DojoMembership.objects.create(
                user=user,
                dojo=dojo,
                role=DojoRole.STUDENT            
            )
            # 🔹 GARANTE EXISTÊNCIA DO DASHBOARD DO DOJO
            Dashboard.objects.get_or_create(
                dojo=dojo,
                defaults={
                    "active_students": 0,
                    "last_exam_participants": 0,
                    "last_exam_approved": 0,
                    "next_exam_registered": 0,
                }
            )

            return karateka

        except IntegrityError as e:
            raise serializers.ValidationError({
                "detail": f"Erro de integridade ao salvar o Karateca: {str(e)}"
            })

