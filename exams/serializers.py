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
    subject_name = serializers.CharField(source="subject.name", read_only=True)
    sensei_examiner_name = serializers.CharField(
        source="sensei_examiner.name", read_only=True
    )

    class Meta:
        model = ExamResult
        fields = [
            "id",
            "subject",
            "subject_id",
            "subject_name",
            "score",
            "comments",
            "sensei_examiner",
            "sensei_examiner_name",
        ]


# -----------------------------------------------------------------------------  
# Serializer para as matérias (requirements) de cada exame  
# -----------------------------------------------------------------------------  
class ExamRequirementWithResultSerializer(serializers.ModelSerializer):
    subject_id = serializers.IntegerField(source="subject.id", read_only=True)
    subject_name = serializers.CharField(source="subject.name", read_only=True)
    score = serializers.SerializerMethodField()

    class Meta:
        model = ExamRequirement
        fields = ["subject_id", "subject_name", "min_score", "max_score", "score"]

    def get_score(self, obj):
        enrollment = self.context.get("enrollment")
        if not enrollment:
            return 0

        result = ExamResult.objects.filter(
            enrollment=enrollment,
            subject=obj.subject
        ).first()

        return result.score if result else 0


# -----------------------------------------------------------------------------  
# Serializer para os participantes do exame  
# -----------------------------------------------------------------------------  
class ExamEnrollmentSerializer(serializers.ModelSerializer):
    karateca_name = serializers.CharField(source="karateca.name", read_only=True)
    karateca_graduation = serializers.CharField(source="karateca.graduation", read_only=True)
    category_name = serializers.CharField(source="category.name", read_only=True)

    subjects = serializers.SerializerMethodField()
    approved = serializers.SerializerMethodField()
    results = ExamResultSerializer(many=True, required=False)

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
        requirements = obj.exam.requirements.all()
        return ExamRequirementWithResultSerializer(
            requirements,
            many=True,
            context={"enrollment": obj}
        ).data

    def get_approved(self, obj):
        requirements = obj.exam.requirements.all()

        if not requirements.exists():
            return False

        for req in requirements:
            result = ExamResult.objects.filter(
                enrollment=obj,
                subject=req.subject
            ).first()
            
            if not result:
                return False
            
            if result.score < req.min_score:
                return False
        return True

    def update(self, instance, validated_data):
        results_data = validated_data.pop("results", None)
        request = self.context.get("request")

        sensei_name = "Desconhecido"
        if request and request.user.is_authenticated:
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
                        "sensei_examiner": sensei_name,
                    },
                )

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

        # 🔹 Atualiza aprovação e graduação
        requirements = instance.exam.requirements.all()

        approved = True
        for req in requirements:
            result = ExamResult.objects.filter(
                enrollment=instance,
                subject=req.subject
            ).first()

            score = result.score if result else 0

            if score < req.min_score:
                approved = False
                break

        instance.approved = approved
        instance.save()

        # 🔹 SE aprovado → atualiza graduação
        if approved and instance.category and instance.category.to_graduation:
            karateca = instance.karateca

            # evita update desnecessário
            if karateca.graduation != instance.category.to_graduation:
                karateca.graduation = instance.category.to_graduation
                karateca.save()


class ExamCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamCategory
        fields = ['id', 'name_category', 'description'] 
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['name'] = instance.name_category
        return data


# -----------------------------------------------------------------------------  
# Serializer principal do exame  
# -----------------------------------------------------------------------------  
class ExamSerializer(serializers.ModelSerializer):
    dojo_name = serializers.CharField(source="dojo.tradename", read_only=True)
    categories = ExamCategorySerializer(many=True, read_only=True)
    participants = serializers.SerializerMethodField()
    selected_category = serializers.SerializerMethodField()

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
            "selected_category",
        ]

    def to_representation(self, instance):
        return super().to_representation(instance)

    def get_participants(self, obj):
        filtered = self.context.get("filtered_participants")
        if filtered is not None:
            return ExamEnrollmentSerializer(filtered, many=True).data
        return ExamEnrollmentSerializer(obj.enrollments.all(), many=True).data

    def get_selected_category(self, obj):
        return self.context.get("selected_category", None)

    def update(self, instance, validated_data):
        request = self.context['request']
        user = getattr(request, "user", None)

        if user and not validated_data.get("sensei_examiner"):
            try:
                sensei = Sensei.objects.get(user=user)
                validated_data["sensei_examiner"] = sensei
            except Sensei.DoesNotExist:
                pass

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


# -------------------------------------------------------------------------
# Serializers de leitura (APP)
# -------------------------------------------------------------------------

class ExamParticipantReadSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source="karateca.name", read_only=True)
    kyu = serializers.CharField(source="karateca.graduation", read_only=True)
    belt = serializers.CharField(source="karateca.graduation", read_only=True)

    class Meta:
        model = ExamEnrollment
        fields = [
            "student_name",
            "kyu",
            "belt",
        ]


class ExamRequirementReadSerializer(serializers.ModelSerializer):
    subject = serializers.CharField(source="subject.name", read_only=True)

    class Meta:
        model = ExamRequirement
        fields = [
            "subject",
            "min_score",
            "max_score",
        ]


class ExamCategoryDetailSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="name_category", read_only=True)
    from_kyu = serializers.SerializerMethodField()
    to_kyu = serializers.SerializerMethodField()
    subjects = serializers.SerializerMethodField()
    registrations = serializers.SerializerMethodField()

    class Meta:
        model = ExamCategory
        fields = [
            "id",
            "name",
            "from_kyu",
            "to_kyu",
            "subjects",
            "registrations",
        ]

    def get_from_kyu(self, obj):
        return obj.from_graduation if hasattr(obj, "from_graduation") else None

    def get_to_kyu(self, obj):
        return obj.to_graduation if hasattr(obj, "to_graduation") else None

    # ✅ CORREÇÃO AQUI (única alteração)
    def get_subjects(self, obj):
        exam = self.context.get("exam")
        requirements = ExamRequirement.objects.filter(
            exam=exam,
            category=obj
        )
        return ExamRequirementReadSerializer(requirements, many=True).data

    def get_registrations(self, obj):
        enrollments = ExamEnrollment.objects.filter(category=obj).select_related(
            "karateca", "karateca__graduation"
        )
        return ExamParticipantReadSerializer(enrollments, many=True).data


class ExamDetailReadSerializer(serializers.ModelSerializer):
    dojo = serializers.CharField(
        source="dojo.tradename",
        read_only=True
    )
    status = serializers.CharField(
        source="get_status_display",
        read_only=True
    )
    categories = serializers.SerializerMethodField()

    class Meta:
        model = Exam
        fields = [
            "id",
            "description",
            "date",
            "status",
            "dojo",
            "categories",
        ]

    def get_categories(self, obj):
        return ExamCategoryDetailSerializer(
            obj.categories.all(),
            many=True,
            context={"exam": obj}
        ).data
