from rest_framework import serializers
from .models import TrainingAttendance


class TrainingAttendanceSerializer(serializers.ModelSerializer):
    karateca_name = serializers.CharField(
        source="karateca.name", read_only=True
    )
    dojo_name = serializers.CharField(
        source="dojo.tradename", read_only=True
    )

    class Meta:
        model = TrainingAttendance
        fields = [
            "id",
            "karateca",
            "karateca_name",
            "dojo",
            "dojo_name",
            "training_date",
            "present",
        ]