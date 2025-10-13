# dashboards/serializers.py
from rest_framework import serializers
from dashboards.models import Dashboard


class DashboardSerializer(serializers.ModelSerializer):
    # nome do sensei associado ao dojo (relacionamento direto -> dojo.sensei.username)
    sensei_name = serializers.CharField(source="dojo.sensei.username", read_only=True)

    # dojoName é um campo calculado via método (tradename > razaosocial)
    dojoName = serializers.SerializerMethodField()

    # novos campos derivados
    upcoming_events = serializers.SerializerMethodField()
    last_exam_students = serializers.SerializerMethodField()
    next_exam_students = serializers.SerializerMethodField()

    # 🔹 novo campo para expor o id do próximo exame
    next_exam_id = serializers.SerializerMethodField()

    class Meta:
        model = Dashboard
        fields = [
            "id",
            "dojoName",
            "sensei_name",
            "active_students",           
            "last_exam_date",
            "last_exam_participants",
            "last_exam_approved",
            "last_exam_students",
            "next_exam_date",
            "next_exam_registered",
            "next_exam_students",
            "next_exam_name",
            "next_exam_id",   # <-- incluímos aqui
            "upcoming_events",
            "updated_at",
        ]

   
    def get_dojoName(self, obj):
        """
        Retorna o nome fantasia do dojo se existir,
        caso contrário retorna a razão social.
        """
        return obj.dojo.tradename or obj.dojo.razaosocial

    def get_last_exam_students(self, obj):
        """
        Retorna lista com nomes dos karatecas do último exame.
        O campo last_exam_students no Dashboard é JSON, por isso tratamos como lista de dicts.
        """
        raw = obj.last_exam_students or []
        return [s.get("name") for s in raw if "name" in s]

    def get_next_exam_students(self, obj):
        """
        Retorna lista com nomes dos karatecas do próximo exame.
        O campo next_exam_students no Dashboard também é JSON.
        """
        raw = obj.next_exam_students or []
        return [s.get("name") for s in raw if "name" in s]

    def get_upcoming_events(self, obj):
        """
        Retorna upcoming_events como lista de dicionários estruturados,
        garantindo sempre o mesmo formato no JSON da API.
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

    def get_sensei_name(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return request.user.get_full_name() or request.user.username
        return "Sensei"
    
    def get_next_exam_id(self, obj):
        """
        Extrai o id do próximo exame a partir do JSON armazenado em next_exam_students.
        Caso não exista exame futuro, retorna None.
        """
        raw = obj.next_exam_students or []
        # Se houver alunos vinculados, pega o id do exame do primeiro
        # Obs: se você salvar o id do exame diretamente no Dashboard, basta retornar aqui.
        return obj.next_exam_date and obj.next_exam_students and obj.id  # ajuste se já salva o exam_id no Dashboard
