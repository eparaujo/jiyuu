# dashboards/serializers.py
from rest_framework import serializers
from dashboards.models import Dashboard


class DashboardSerializer(serializers.ModelSerializer):
    # nome do sensei associado ao dojo
    senseiName = serializers.CharField(source="dojo.sensei.username", read_only=True)

    # dojoName é um campo calculado via método
    dojoName = serializers.SerializerMethodField()

    def get_dojoName(self, obj):
        # retorna nome fantasia se existir, senão razão social
        return obj.dojo.tradename or obj.dojo.razaosocial

    # campos calculados a partir dos JSONFields
    upcoming_events = serializers.SerializerMethodField()
    last_exam_students = serializers.SerializerMethodField()
    next_exam_students = serializers.SerializerMethodField()

    class Meta:
        model = Dashboard
        fields = [
            "id",
            "dojo",
            "dojoName",
            "senseiName",
            "active_students",           
            "last_exam_date",
            "last_exam_participants",
            "last_exam_approved",
            "last_exam_students",
            "next_exam_date",
            "next_exam_registered",
            "next_exam_students",
            "next_exam_name",
            "upcoming_events",
            "updated_at",
        ]

    def get_last_exam_students(self, obj):
        """
        Retorna somente a lista de nomes dos karatecas do último exame.
        """
        raw = obj.last_exam_students or []
        return [s.get("name") for s in raw if "name" in s]

    def get_next_exam_students(self, obj):
        """
        Retorna somente a lista de nomes dos karatecas do próximo exame.
        """
        raw = obj.next_exam_students or []
        return [s.get("name") for s in raw if "name" in s]

    def get_upcoming_events(self, obj):
        """
        Retorna upcoming_events como lista de dicionários estruturados.
        """
        raw = obj.upcoming_events or []
        structured = []
        for e in raw:
            structured.append(
                {
                    "id": e.get("id"),
                    "name": e.get("name"),
                    "date": e.get("date"),
                    "description": e.get("description"),
                    "organizer": e.get("organizer", ""),
                }
            )
        return structured
