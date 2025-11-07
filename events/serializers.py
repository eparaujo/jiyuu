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
    category = CategorySerializer(many=True, read_only=True)
    modality = ModalitySerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = "__all__"


class CourseEnrollmentSerializer(serializers.ModelSerializer):
    karateca_name = serializers.CharField(source="karateca.name", read_only=True)
    event_name = serializers.CharField(source="event.name", read_only=True)

    class Meta:
        model = CourseEnrollment
        fields = [
            "id", "event", "event_name", "karateca", "karateca_name",
            "enrollment_date", "paid"
        ]
