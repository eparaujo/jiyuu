from rest_framework import serializers
from .models import Exam, ExamEnrollment, ExamResult


class ExamEnrollmentSerializer(serializers.ModelSerializer):
    karateca_name = serializers.CharField(source="karateca.name", read_only=True)
    karateca_graduation = serializers.CharField(
        source="karateca.graduation.belt",
        read_only=True
    )
    # ✅ approved agora é campo real, pode ser editado também
    class Meta:
        model = ExamEnrollment
        fields = ["id", "karateca", "karateca_name", "karateca_graduation", "approved"]


class ExamResultSerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(source="subject.name", read_only=True)

    class Meta:
        model = ExamResult
        fields = ["id", "subject", "subject_name", "score"]


class ExamSerializer(serializers.ModelSerializer):
    dojo_name = serializers.CharField(source="dojo.tradename", read_only=True)
    participants = ExamEnrollmentSerializer(
        source="enrollments",
        many=True,
        read_only=True
    )

    class Meta:
        model = Exam
        fields = [
            "id",
            "dojo",
            "dojo_name",
            "date",
            "description",
            "participants",
        ]
