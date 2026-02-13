from rest_framework import serializers
from .models import Exam, ExamEnrollment, ExamResult, ExamRequirement, ExamCategory
from senseis.models import Sensei
from dojos.models import DojoMembership
from dojos.choices import DojoRole
from rest_framework.exceptions import PermissionDenied


 
# -----------------------------------------------------------------------------  
# Serializer para resultados individuais (input/output das notas e comentários)  
# -----------------------------------------------------------------------------  
class ExamResultSerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(source="subject.name", read_only=True)  # nome da matéria
    sensei_examiner_name = serializers.CharField(
        source="sensei_examiner.name", read_only=True
    )  # nome do examinador (sensei responsável)

    class Meta:
        model = ExamResult
        fields = [
            "id",
            "subject",
            "subject_id",
            "subject_name",
            "score",
            "comments",
            "sensei_examiner",         # 🔹 campo de vínculo (para gravação)
            "sensei_examiner_name",    # 🔹 campo auxiliar somente leitura
        ]


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
    karateca_name = serializers.CharField(source="karateca.name", read_only=True)
    karateca_graduation = serializers.CharField(source="karateca.graduation", read_only=True)
    
    # 🔹 Categoria do exame (FK -> ExamCategory)
    category_name = serializers.CharField(source="category.name", read_only=True)
    
    subjects = serializers.SerializerMethodField()  # matérias + notas (somente leitura)
    approved = serializers.SerializerMethodField()  # calculado dinamicamente
    results = ExamResultSerializer(many=True, required=False)  # leitura/escrita

    class Meta:
        model = ExamEnrollment
        fields = [
            "id",
            "karateca",
            "karateca_name",
            "karateca_graduation",
            "category_name",
            "approved",
            "subjects",
            "results",
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
            context={"enrollment": obj}
        ).data

    def get_approved(self, obj):
        """
        Calcula se o karateca foi aprovado:
        - aprovado se TODAS as notas >= min_score
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
        Também grava o nome do sensei examinador autenticado.
        """
        results_data = validated_data.pop("results", None)
        request = self.context.get("request")

        sensei_name = "Desconhecido"
        if request and hasattr(request, "user") and request.user.is_authenticated:
            sensei_name = request.user.get_full_name() or request.user.username

        # 🔹 Atualiza ou cria os resultados por matéria
        if results_data:
            for result_data in results_data:
                subject = result_data["subject"]
                score = result_data.get("score", 0)
                comments = result_data.get("comments", "")

                ExamResult.objects.update_or_create(
                    enrollment=instance,
                    subject=subject,
                    defaults={
                        "score": score,
                        "comments": comments,
                        "sensei_examiner": sensei_name,
                    },
                )

        # 🔹 Atualiza apenas campos simples do Enrollment (sem quebrar relações)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


    """def update(self, instance, validated_data):
        
        #Atualiza notas (results) do participante.
        #Também grava o nome do sensei examinador autenticado.
        
        results_data = validated_data.pop("results", None)
        request = self.context.get("request")
        
        sensei_name = "Desconhecido"
        if request and hasattr(request, "user") and request.user.is_authenticated:
            sensei_name = request.user.get_full_name() or request.user.username

        if results_data:
            for result_data in results_data:
                subject = result_data["subject"]
                score = result_data.get("score", 0)
                comments = result_data.get("comments", "")

                ExamResult.objects.update_or_create(
                    enrollment=instance,
                    subject=subject,
                    defaults={
                        "score": score,
                        "comments": comments,
                        "sensei_examiner": sensei_name
                    }
                )

        return super().update(instance, validated_data)"""



class ExamCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamCategory
        fields = ['id', 'name_category', 'description'] 
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        # 🔹 Renomeia o campo para "name" (compatível com Flutter)
        data['name'] = instance.name_category
        return data


# -----------------------------------------------------------------------------  
# Serializer principal do exame  
# -----------------------------------------------------------------------------  
class ExamSerializer(serializers.ModelSerializer):
    dojo_name = serializers.CharField(source="dojo.tradename", read_only=True)
    categories = ExamCategorySerializer(many=True, read_only=True)
    participants = serializers.SerializerMethodField()
    selected_category = serializers.SerializerMethodField()  # ✅ nome da categoria filtrada (útil no Flutter)

    sensei_examiner = serializers.PrimaryKeyRelatedField(
        queryset=Sensei.objects.all(),
        required=False,
        allow_null=True
    )

    class Meta:
        model = Exam
        fields = [
            "id",
            "dojo",
            "dojo_name",
            "date",
            "description",
            "status",
            "sensei_examiner",
            "categories",
            "participants",
            "selected_category",  # ✅ novo campo retornado no JSON
        ]

    # --- método abaixo das funções get_* ---
    def to_representation(self, instance):
        """
        Intercepta a saída final antes de enviar o JSON.
        Ideal para debug e análise de dados enviados ao Flutter.
        """
        data = super().to_representation(instance)
        #print("\n🔍 JSON retornado para o Flutter:")
        import json
        #print(json.dumps(data, indent=4, ensure_ascii=False))
        return data
        
    # -------------------------------------------------------------------------
    # ✅ Retorna lista filtrada de participantes (por categoria, se houver)
    # -------------------------------------------------------------------------
    def get_participants(self, obj):
        filtered = self.context.get("filtered_participants")
        if filtered is not None:
            # 🔹 Endpoint filtrado: /categories/<id>/participants/
            return ExamEnrollmentSerializer(filtered, many=True).data
        # 🔹 Endpoint normal: retorna todos os participantes
        return ExamEnrollmentSerializer(obj.enrollments.all(), many=True).data

    # -------------------------------------------------------------------------
    # ✅ Retorna o nome da categoria selecionada (usado no app Flutter)
    # -------------------------------------------------------------------------
    def get_selected_category(self, obj):
        return self.context.get("selected_category", None)

    # -------------------------------------------------------------------------
    # ✅ Atualização de exame + participantes
    # -------------------------------------------------------------------------
    def update(self, instance, validated_data):
        request = self.context['request']
        user = getattr(request, "user", None)

        # 🔹 Se o usuário for um Sensei, associa automaticamente como examinador
        if user and not validated_data.get("sensei_examiner"):
            try:
                sensei = Sensei.objects.get(user=user)
                validated_data["sensei_examiner"] = sensei
            except Sensei.DoesNotExist:
                pass  # Usuário não é um sensei

        # 🔹 Atualiza participantes, se enviados
        participants_data = request.data.get("participants", None)
        if participants_data:
            for participant_data in participants_data:
                participant_id = participant_data.get("id")
                if participant_id:
                    enrollment = ExamEnrollment.objects.get(id=participant_id)
                    serializer = ExamEnrollmentSerializer(
                        enrollment,
                        data=participant_data,
                        partial=True,
                        context={'request': request}
                    )
                    serializer.is_valid(raise_exception=True)
                    serializer.save()

        instance.save()
        return super().update(instance, validated_data)
