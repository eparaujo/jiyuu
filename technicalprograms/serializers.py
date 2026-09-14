from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from .models import TechnicalProgram, TechnicalProgramItem


class TechnicalProgramItemSerializer(serializers.ModelSerializer):
    modality_display = serializers.CharField(
        source="get_modality_display",
        read_only=True,
    )

    class Meta:
        model = TechnicalProgramItem

        fields = [
            "id",
            "modality",
            "modality_display",
            "title",
            "description",
            "sequence",
            "mandatory",
            "active",
        ]

        
class TechnicalProgramSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(
        source="category.name_category",
        read_only=True,
    )

    style = serializers.CharField(
        source="get_style_display",
        read_only=True
    )

    target = serializers.SerializerMethodField()

    items = TechnicalProgramItemSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = TechnicalProgram

        fields = [
            "id",
            "category",
            "category_name",
            "style",
            "target",
            "description",
            "active",
            "items",
        ]

    def get_target(self, obj):
        """
        Monta automaticamente o percurso da graduação anterior
        para a graduação de destino do programa.
        """

        if not obj.category or not obj.category.to_graduation:
            return None

        to_graduation = obj.category.to_graduation

        # Busca a graduação imediatamente anterior
        from graduations.models import Graduation

        from_graduation = (
            Graduation.objects
            .filter(
                order__lt=to_graduation.order
            )
            .order_by("-order", "-id")
            .first()
        )

        if not from_graduation:
            return to_graduation.name

        return f"{from_graduation.name} → {to_graduation.name}"