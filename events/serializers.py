from rest_framework import serializers
from .models import Event, CourseEnrollment, Category, Modality
from karatecas.models import Karateca


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class ModalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Modality
        fields = ["id", "name"]


class EventSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    modality = serializers.SerializerMethodField()
    hability_graduation = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = "__all__"

    def get_category(self, obj):
        return [
            category.name
            for category in obj.category.all().order_by("name")
        ]

    def get_modality(self, obj):
        return [
            modality.name
            for modality in obj.modality.all().order_by("name")
        ]

    def get_hability_graduation(self, obj):
        graduations = obj.hability_graduation.all().order_by("order")

        result = []

        for graduation in graduations:
            name = graduation.name.strip()

            # Exemplo:
            # "6º Kyu - Faixa Amarela"
            # vira:
            # "Faixa Amarela"
            if " - " in name:
                _, faixa = name.split(" - ", 1)
                result.append(faixa)
            else:
                result.append(name)

        return result


class CourseEnrollmentSerializer(serializers.ModelSerializer):
    karateca_name = serializers.CharField(source="karateca.name", read_only=True)
    event_name = serializers.CharField(source="event.name", read_only=True)

    class Meta:
        model = CourseEnrollment
        fields = [
            "id", "event", "event_name", "karateca", "karateca_name",
            "enrollment_date", "paid"
        ]
