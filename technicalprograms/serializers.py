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