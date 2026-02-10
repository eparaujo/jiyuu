# serializers.py
from rest_framework import serializers
from .models import Dojo
from dojos.models import DojoMembership
from dojos.choices import DojoRole


class DojoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dojo
        fields = ['id', 'tradename']

# serializer para definir role
class ChangeRoleSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    dojo_id = serializers.IntegerField()
    role = serializers.ChoiceField(choices=DojoRole.choices)

    def validate(self, attrs):
        request = self.context["request"]
        acting_user = request.user

        user_id = attrs["user_id"]
        dojo_id = attrs["dojo_id"]
        new_role = attrs["role"]

        if acting_user.id == user_id:
            raise serializers.ValidationError("Você não pode alterar sua própria role.")

        try:
            actor_membership = DojoMembership.objects.get(
                user=acting_user,
                dojo_id=dojo_id
            )
        except DojoMembership.DoesNotExist:
            raise serializers.ValidationError("Você não pertence a este dojo.")

        if actor_membership.role not in [DojoRole.OWNER, DojoRole.ADMIN]:
            raise serializers.ValidationError("Permissão negada.")

        if actor_membership.role == DojoRole.ADMIN and new_role == DojoRole.OWNER:
            raise serializers.ValidationError("ADMIN não pode promover para OWNER.")

        try:
            target_membership = DojoMembership.objects.get(
                user_id=user_id,
                dojo_id=dojo_id
            )
        except DojoMembership.DoesNotExist:
            raise serializers.ValidationError("Usuário alvo não pertence a este dojo.")

        if target_membership.role == DojoRole.OWNER:
            raise serializers.ValidationError("OWNER não pode ser alterado.")

        attrs["target_membership"] = target_membership
        return attrs
    
# dojos/serializers.py
class DojoMemberSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source="user.id")
    name = serializers.CharField(source="user.get_full_name")
    email = serializers.EmailField(source="user.email")

    class Meta:
        model = DojoMembership
        fields = [
            "id",
            "user_id",
            "name",
            "email",
            "role",
        ]

# dojos/serializers.py
class DojoMemberListSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="user.first_name")
    email = serializers.EmailField(source="user.email")

    class Meta:
        model = DojoMembership
        fields = [
            "id",
            "name",
            "email",
            "role",
            "active",
        ]


class DojoMemberRoleUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DojoMembership
        fields = ["role"]

class DojoMemberActiveUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DojoMembership
        fields = ["active"]
