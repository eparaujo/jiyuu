# exams/views.py
from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView, View
from django.urls import reverse_lazy
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.mixins import LoginRequiredMixin
from . import models, forms
from rest_framework import generics
from . import serializers
from .serializers import ExamResultSerializer, ExamRequirementWithResultSerializer, ExamEnrollmentSerializer, ExamSerializer, ExamEnrollmentSerializer, ExamDetailReadSerializer
from rest_framework.views import APIView
from .models import ExamEnrollment, Exam, ExamCategory, ExamRequirement, ExamResult
from examcategories.models import ExamCategory
from senseis.models import Sensei
from django.shortcuts import get_object_or_404
from exams.permissions import IsOwnerOrExaminer
from rest_framework.permissions import IsAuthenticated
from collections import OrderedDict
from rest_framework.generics import RetrieveAPIView
from .permissions import IsExamStudent
from rest_framework.exceptions import NotFound
from dojos.models import DojoMembership
from trainings.services import can_do_exam
from django.contrib import messages
from .forms import ExamEnrollmentForm
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from datetime import timedelta


# -------------------------------
# EXAM
# -------------------------------
class ExamListView(LoginRequiredMixin, ListView):
    model = models.Exam
    template_name = "exam_list.html"
    context_object_name = "exams"
    paginate_by = 10

    def get_queryset(self): 
        queryset = super().get_queryset()
        description = self.request.GET.get("description")
        if description:
            queryset = queryset.filter(description__icontains=description)
        return queryset
 
 
class ExamCreateView(LoginRequiredMixin, CreateView):
    model = models.Exam
    template_name = "exam_create.html"
    form_class = forms.ExamForm
    success_url = reverse_lazy("exam_list")


class ExamDetailView(LoginRequiredMixin, DetailView):
    model = models.Exam
    template_name = "exam_detail.html"

    def get_queryset(self):
        """
        Otimiza o carregamento do exame e seus relacionamentos
        para evitar múltiplas queries no template.
        """
        return (
            super()
            .get_queryset()
            .select_related("dojo")
            .prefetch_related(
                "categories",
                "requirements__subject",
                "requirements__category",
                "enrollments__karateca",
                "enrollments__current_graduation",
                "enrollments__category",
            )
        )

    def get_context_data(self, **kwargs):
        """
        Contexto adicional preparado para futuras etapas
        (ex: verificação de elegibilidade para o exame).
        """
        context = super().get_context_data(**kwargs)

        exam = self.object

        # 🔹 Inscrições já existentes (organizadas por categoria no template)
        context["enrollments"] = exam.enrollments.all()

        # 🔹 Requisitos do exame
        context["requirements"] = exam.requirements.all()

        # 🔹 Categorias do exame
        context["categories"] = exam.categories.all()

        return context


class ExamUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Exam
    template_name = "exam_update.html"
    form_class = forms.ExamForm
    success_url = reverse_lazy("exam_list")


class ExamDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Exam
    template_name = "exam_delete.html"
    success_url = reverse_lazy("exam_list")


class ExamDetailAPIView(LoginRequiredMixin, APIView):
    """
    Retorna os dados completos de um exame em formato JSON,
    incluindo inscritos e matérias com notas mínimas e máximas.
    """

    def get(self, request, pk):
        try:
            # Busca o exame pelo ID
            exam = models.Exam.objects.get(pk=pk)
        except models.Exam.DoesNotExist:
            return Response({"error": "Exame não encontrado"}, status=status.HTTP_404_NOT_FOUND)

        # Monta lista de requisitos (matérias do exame)
        requirements = []
        for req in exam.requirements.all():
            requirements.append({
                "id": req.id,
                "subject": req.subject.name,
                "min_score": req.min_score,
                "max_score": req.max_score,
            })

        # Monta lista de karatecas inscritos
        participants = []
        for enrollment in exam.enrollments.all():
            participants.append({
                "id": enrollment.karateca.id,
                "name": str(enrollment.karateca),
                "subjects": requirements,  # Cada karateca tem as mesmas matérias definidas para o exame
            })

        # Estrutura final do JSON
        data = {
            "id": exam.id,
            "date": exam.date,
            "name": exam.description,
            "participants": participants,
        }

        return Response(data, status=status.HTTP_200_OK)


# -------------------------------
# EXAM SUBJECT
# -------------------------------
class ExamSubjectListView(LoginRequiredMixin, ListView):
    model = models.ExamSubject
    template_name = "subject_list.html"
    context_object_name = "subjects"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get("name")
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset


class ExamSubjectCreateView(LoginRequiredMixin, CreateView):
    model = models.ExamSubject
    template_name = "subject_create.html"
    form_class = forms.ExamSubjectForm
    success_url = reverse_lazy("subject_list")


class ExamSubjectDetailView(LoginRequiredMixin, DetailView):
    model = models.ExamSubject
    template_name = "subject_detail.html"


class ExamSubjectUpdateView(LoginRequiredMixin, UpdateView):
    model = models.ExamSubject
    template_name = "subject_update.html"
    form_class = forms.ExamSubjectForm
    success_url = reverse_lazy("subject_list")


class ExamSubjectDeleteView(LoginRequiredMixin, DeleteView):
    model = models.ExamSubject
    template_name = "subject_delete.html"
    success_url = reverse_lazy("subject_list")


# -------------------------------
# EXAM REQUIREMENT
# -------------------------------
class ExamRequirementListView(LoginRequiredMixin, ListView):
    model = models.ExamRequirement
    template_name = "requirement_list.html"
    context_object_name = "requirements"
    paginate_by = 10
    
    def get_queryset(self):
        queryset = super().get_queryset()
        subject = self.request.GET.get("subject")
        if subject:
            queryset = queryset.filter(subject__name__icontains=subject)
        return queryset


class ExamRequirementCreateView(LoginRequiredMixin, CreateView):
    model = models.ExamRequirement
    template_name = "requirement_create.html"
    form_class = forms.ExamRequirementForm
    success_url = reverse_lazy("requirement_list")


class ExamRequirementDetailView(LoginRequiredMixin, DetailView):
    model = models.ExamRequirement
    template_name = "requirement_detail.html"


class ExamRequirementUpdateView(LoginRequiredMixin, UpdateView):
    model = models.ExamRequirement
    template_name = "requirement_update.html"
    form_class = forms.ExamRequirementForm
    success_url = reverse_lazy("requirement_list")


class ExamRequirementDeleteView(LoginRequiredMixin, DeleteView):
    model = models.ExamRequirement
    template_name = "requirement_delete.html"
    success_url = reverse_lazy("requirement_list")


# -------------------------------
# EXAM ENROLLMENT LIST VIEW
# -------------------------------
class ExamEnrollmentListView(LoginRequiredMixin, ListView):
    model = ExamEnrollment
    template_name = "enrollment_list.html"
    context_object_name = "enrollments"

    def get_queryset(self):
        self.exam = get_object_or_404(Exam, pk=self.kwargs["exam_id"])
        queryset = ExamEnrollment.objects.filter(exam=self.exam)

        karateca = self.request.GET.get("karateca")
        if karateca:
            queryset = queryset.filter(karateca__name__icontains=karateca)

        return queryset.select_related(
            "karateca", "current_graduation", "category"
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["exam"] = self.exam
        return context

class ExamEnrollmentCreateView(LoginRequiredMixin, CreateView):
    model = ExamEnrollment
    template_name = "enrollment_create.html"
    form_class = ExamEnrollmentForm
    success_url = reverse_lazy("exam_list")

    def get_form_kwargs(self):
        """
        Injeta o exame no form para GET e POST
        """
        kwargs = super().get_form_kwargs()
        exam_id = self.kwargs.get("exam_id")

        self.exam = models.Exam.objects.select_related("dojo").get(pk=exam_id)
        kwargs["exam"] = self.exam

        return kwargs

    def form_valid(self, form):
        """
        Validação central de negócio:
        impede inscrição se karateca estiver em carência
        """

        # 🔒 GARANTE o vínculo correto
        form.instance.exam = self.exam

        karateca = form.cleaned_data.get("karateca")

        # 🔒 REGRA DE NEGÓCIO (ETAPA 7)
        can_exam, reason = can_do_exam(karateca)
        if not can_exam:
            messages.error(self.request, reason)
            return self.form_invalid(form)

        # Evita inscrição duplicada
        if ExamEnrollment.objects.filter(
            exam=self.exam,
            karateca=karateca
        ).exists():
            messages.warning(
                self.request,
                "Este karateca já está inscrito neste exame."
            )
            return self.form_invalid(form)

        messages.success(
            self.request,
            "Karateca inscrito com sucesso no exame."
        )
        return super().form_valid(form)
    

class ExamEnrollmentDetailView(LoginRequiredMixin, DetailView):
    model = models.ExamEnrollment
    template_name = "enrollment_detail.html"


class ExamEnrollmentUpdateView(LoginRequiredMixin, UpdateView):
    model = models.ExamEnrollment
    template_name = "enrollment_update.html"
    form_class = forms.ExamEnrollmentForm
    success_url = reverse_lazy("enrollment_list")


class ExamEnrollmentDeleteView(LoginRequiredMixin, DeleteView):
    model = models.ExamEnrollment
    template_name = "enrollment_delete.html"
    success_url = reverse_lazy("enrollment_list")

# -------------------------------
# VISUALIZAR KARATECAS INSCRITOS POR CATEGORIA DE GRADUAÇÃO
# -------------------------------

class ExamParticipantsByCategoryView(LoginRequiredMixin, View):
    template_name = "exam_participants_by_category.html"

    def get(self, request, pk, category):
        exam = get_object_or_404(models.Exam, id=pk)
        participants = models.ExamEnrollment.objects.filter(
            exam=exam,
            category__name__iexact=category  # compara ignorando maiúsculas/minúsculas
        ).select_related("karateca", "karateca__graduation", "category")

        context = {
            "exam": exam,
            "category": category.capitalize(),
            "participants": participants,
        }
        return render(request, self.template_name, context)



# -------------------------------
# EXAM RESULT
# -------------------------------
class ExamResultListView(LoginRequiredMixin, ListView):
    """
    Lista os resultados de exame agrupados por karateca.
    Observação: o campo `sensei_examiner` em ExamResult é um CharField (nome do avaliador),
    portanto tratamos como string na exibição.
    """
    model = models.ExamResult
    template_name = "result_list.html"
    context_object_name = "results"
    paginate_by = 15

    def get_queryset(self):
        """
        Retorna queryset otimizado (evita N+1) e aplica filtros opcionais.
        """
        queryset = (
            super()
            .get_queryset()
            .select_related(
                "enrollment__karateca",  # FK real: traz dados do karateca
                "subject"                # FK real: traz dados da matéria
            )
            .order_by("enrollment__karateca__name", "subject__name")
        )

        # filtro opcional por nome da matéria
        subject = self.request.GET.get("subject")
        if subject:
            queryset = queryset.filter(subject__name__icontains=subject)

        return queryset

    def get_context_data(self, **kwargs):
        """
        Agrupa os resultados por karateca e coloca em `karateca_list`
        no formato que seu template espera: [{'grouper': karateca, 'list': [...]}, ...]
        """
        context = super().get_context_data(**kwargs)
        results_page = context.get(self.context_object_name, [])

        grouped = OrderedDict()
        for result in results_page:
            # enrollment.karateca é a instância do Karateca (objeto)
            karateca = result.enrollment.karateca
            grouped.setdefault(karateca, []).append(result)

        # transforma em lista de dicionários para o template
        context["karateca_list"] = [{"grouper": k, "list": v} for k, v in grouped.items()]
        return context
    

class ExamResultCreateView(LoginRequiredMixin, CreateView):
    model = models.ExamResult
    template_name = "result_create.html"
    form_class = forms.ExamResultForm
    success_url = reverse_lazy("result_list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        enrollment_id = self.request.GET.get("enrollment")

        if enrollment_id:
            try:
                enrollment = models.ExamEnrollment.objects.select_related("exam__dojo").get(id=enrollment_id)

                # 🔹 injeta instance já com enrollment (EVITA ERRO)
                kwargs["instance"] = models.ExamResult(enrollment=enrollment)

            except models.ExamEnrollment.DoesNotExist:
                pass

        return kwargs

    def get_initial(self):
        initial = super().get_initial()
        enrollment_id = self.request.GET.get("enrollment")

        if enrollment_id:
            initial["enrollment"] = enrollment_id

        return initial

    def form_valid(self, form):
        enrollment_id = self.request.GET.get("enrollment")

        if enrollment_id:
            form.instance.enrollment_id = enrollment_id

        return super().form_valid(form)


class ExamResultDetailView(LoginRequiredMixin, DetailView):
    model = models.ExamResult
    template_name = "result_detail.html"


class ExamResultUpdateView(LoginRequiredMixin, UpdateView):
    model = models.ExamResult
    template_name = "result_update.html"
    form_class = forms.ExamResultForm
    success_url = reverse_lazy("result_list")


class ExamResultDeleteView(LoginRequiredMixin, DeleteView):
    model = models.ExamResult
    template_name = "result_delete.html"
    success_url = reverse_lazy("result_list")


class ExamRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Exam.objects.all()
    serializer_class = serializers.ExamSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrExaminer]
    

class ExamCreateListAPIView(generics.ListCreateAPIView):
    """
    GET: Lista todos os exames.
    POST: Cria um novo exame.
    """
    queryset = models.Exam.objects.all()
    serializer_class = serializers.ExamSerializer

    
 # API específica para salvar notas de um participante
class ExamEnrollmentUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = ExamEnrollment.objects.all()
    serializer_class = ExamEnrollmentSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrExaminer]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context 
    

class ExamCategoryListAPIView(generics.ListAPIView):
    """
    Retorna as categorias associadas a um exame específico.
    """
    serializer_class = serializers.ExamCategorySerializer

    def get_queryset(self):
        exam_id = self.kwargs["pk"]
        exam = Exam.objects.filter(id=exam_id).first()
        if exam:
            return exam.categories.all() #usa o ManyToMany do model exam 
        return models.ExamCategory.objects.filter(exam__id=exam_id)
    

class ExamParticipantsByCategoryAPIView(generics.ListAPIView):
    """
    Retorna os participantes de um exame filtrados por categoria (ExamCategory).
    Endpoint: /api/v1/exams/<exam_id>/categories/<category_name>/participants/
    """
    serializer_class = ExamEnrollmentSerializer

    def get_queryset(self):
        exam_id = self.kwargs.get("pk")
        category_name = self.kwargs.get("category")  # string enviada pelo Flutter
        print("📩 Categoria recebida do Flutter:", category_name)

        # Garante que o exame existe
        exam = get_object_or_404(Exam, id=exam_id)

        # 🔹 Filtra inscrições pela categoria (ExamCategory.name_category)
        queryset = ExamEnrollment.objects.filter(
            exam=exam,
            category__name_category__iexact=category_name
        ).select_related("karateca", "karateca__graduation", "category") \
         .order_by("karateca__name")  # opcional: ordena alfabeticamente

        print(f"🔎 Total encontrados para {category_name}: {queryset.count()}")
        print("Nome dos karatecas encontrados; ", queryset)
        return queryset


#--------------------------------------
# Último resultado do exame do aluno
#-------------------------------------


class LastExamResultView(APIView):
    permission_classes = [IsAuthenticated]


    def get(self, request):
        karateca = request.user.karateka

        enrollment = (
            ExamEnrollment.objects
            .filter(
                karateca=karateca,
                exam__status="FINALIZADO"
            )
            .select_related("exam")
            .order_by("-exam__date")
            .first()
        )

        if not enrollment:
            return Response({"detail": "Nenhum exame encontrado."})

        results = ExamResult.objects.filter(enrollment=enrollment)

        return Response({
            "exam_id": enrollment.exam.id,
            "exam_date": enrollment.exam.date,
            "subjects": [
                {
                    "name": r.subject.name,
                    "score": r.score
                } for r in results
            ]
        })

#------------------------------------------------
# Detalhes do último resultado do exame do aluno
#------------------------------------------------
class LastExamResultDetailView(APIView):
    permission_classes = [IsAuthenticated]

    print("Entrando no resultado do exame")

    def get(self, request):
        karateca = request.user.karateca

        enrollment = (
            ExamEnrollment.objects
            .filter(
                karateca=karateca,
                exam__status="FINALIZADO"
            )
            .select_related("exam", "category")
            .order_by("-exam__date")
            .first()
        )

        if not enrollment:
            return Response({"detail": "Nenhum exame encontrado."})

        results = ExamResult.objects.filter(enrollment=enrollment)

        return Response({
            "exam": {
                "date": enrollment.exam.date,
                "category": enrollment.category.name if enrollment.category else None
            },
            "subjects": [
                {
                    "name": r.subject.name,
                    "score": r.score,
                    "comments": r.comments
                } for r in results
            ]
        })


# ------------------------------------------------
# Detalhes do exame - leitura para ALUNO (APP)
# ------------------------------------------------
class NextExamAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        membership = (
            DojoMembership.objects
            .select_related("dojo")
            .filter(user=user)
            .first()
        )

        if not membership:
            return Response(
                {"detail": "Usuário sem vínculo com dojo"},
                status=status.HTTP_403_FORBIDDEN
            )

        dojo = membership.dojo

        exam = (
            Exam.objects
            .filter(
                dojo=dojo,
                status='CONFIRMADO'
            )
            .first()
        )

        if not exam:
            return Response(
                {"detail": "Nenhum exame ativo"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ExamDetailReadSerializer(exam)
        return Response(serializer.data)
