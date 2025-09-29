from rest_framework import serializers
from .models import Exam, ExamEnrollment, ExamResult, ExamRequirement


# -----------------------------------------------------------------------------  
# Serializer para resultados individuais (input/output das notas e comentários)  
# -----------------------------------------------------------------------------  
class ExamResultSerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(source="subject.name", read_only=True)  # nome da matéria

    class Meta:
        model = ExamResult
        fields = ["id", "subject", "subject_id", "subject_name", "score", "comments"]


# -----------------------------------------------------------------------------  
# Serializer para as matérias (requirements) de cada exame  
# -----------------------------------------------------------------------------  
class ExamRequirementWithResultSerializer(serializers.ModelSerializer):
    subject_id = serializers.IntegerField(source="subject.id", read_only=True)  # 🔹 ID real da matéria
    subject_name = serializers.CharField(source="subject.name", read_only=True)  # nome da matéria (ex: Kihon, Kata)
    score = serializers.SerializerMethodField()  # nota do karateca (ou 0 se não existir)

    class Meta:
        model = ExamRequirement
        fields = ["subject_id", "subject_name", "min_score", "max_score", "score"]

    def get_score(self, obj):
        """
        Retorna a nota real do karateca para esta matéria.
        Se não existir resultado, retorna 0.
        """
        enrollment = self.context.get("enrollment")  # inscrição do karateca (passada pelo serializer pai)

        if not enrollment:
            return 0

        result = ExamResult.objects.filter(
            enrollment=enrollment,
            subject=obj.subject
        ).first()

        return result.score if result else 0


# -----------------------------------------------------------------------------  
# Serializer para os participantes do exame (karatecas inscritos)  
# -----------------------------------------------------------------------------  
class ExamEnrollmentSerializer(serializers.ModelSerializer):
    karateca_name = serializers.CharField(source="karateca.name", read_only=True)  # nome do karateca
    karateca_graduation = serializers.CharField(
        source="karateca.graduation.belt",
        read_only=True
    )  # graduação atual do karateca
    subjects = serializers.SerializerMethodField()  # matérias + notas (somente leitura)
    approved = serializers.SerializerMethodField()  # calculado dinamicamente
    results = ExamResultSerializer(many=True, required=False)  # 🔹 para leitura/escrita de notas

    class Meta:
        model = ExamEnrollment
        fields = [
            "id",
            "karateca",
            "karateca_name",
            "karateca_graduation",
            "approved",
            "subjects",   # leitura
            "results",    # escrita
        ]

    def get_subjects(self, obj):
        """
        Retorna a lista de matérias exigidas no exame,
        incluindo notas do karateca (se houver).
        """
        requirements = obj.exam.requirements.all()
        return ExamRequirementWithResultSerializer(
            requirements,
            many=True,
            context={"enrollment": obj}  # passamos a inscrição atual para buscar resultados
        ).data

    def get_approved(self, obj):
        """
        Calcula se o karateca foi aprovado:
        - aprovado se TODAS as notas >= min_score
        - caso contrário, reprovado
        """
        requirements = obj.exam.requirements.all()
        for req in requirements:
            result = ExamResult.objects.filter(
                enrollment=obj,
                subject=req.subject
            ).first()

            score = result.score if result else 0
            if score < req.min_score:
                return False
        return True

    def update(self, instance, validated_data):
        """
        Atualiza notas (results) do participante.
        """
        results_data = validated_data.pop("results", None)

        if results_data:
            for result_data in results_data:
                subject = result_data["subject"]
                score = result_data.get("score", 0)
                comments = result_data.get("comments", "")

                ExamResult.objects.update_or_create(
                    enrollment=instance,
                    subject=subject,
                    defaults={"score": score, "comments": comments}
                )

        return super().update(instance, validated_data)


# -----------------------------------------------------------------------------  
# Serializer principal do exame  
# -----------------------------------------------------------------------------  
class ExamSerializer(serializers.ModelSerializer):
    dojo_name = serializers.CharField(source="dojo.tradename", read_only=True)
    participants = ExamEnrollmentSerializer(
        source="enrollments",
        many=True,
        read_only=True  # 🔹 evita AssertionError
    )

    class Meta:
        model = Exam
        fields = ["id", "dojo", "dojo_name", "date", "description", "participants"]

    def update(self, instance, validated_data):
        """
        Atualiza participantes e seus resultados via nested manual.
        """
        participants_data = self.context['request'].data.get("participants", None)  # ✅ pega do request.data

        if participants_data:
            for participant_data in participants_data:
                participant_id = participant_data.get("id")
                if participant_id:
                    enrollment = ExamEnrollment.objects.get(id=participant_id)
                    serializer = ExamEnrollmentSerializer(
                        enrollment,
                        data=participant_data,
                        partial=True,
                        context={'request': self.context['request']}
                    )
                    serializer.is_valid(raise_exception=True)
                    serializer.save()

        return super().update(instance, validated_data)
