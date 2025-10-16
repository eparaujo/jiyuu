# exams/views.py
from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from django.urls import reverse_lazy
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.mixins import LoginRequiredMixin
from . import models, forms
from rest_framework import generics
from . import serializers
from .serializers import ExamResultSerializer, ExamRequirementWithResultSerializer, ExamEnrollmentSerializer, ExamSerializer, ExamEnrollmentSerializer
from rest_framework.views import APIView
from .models import ExamEnrollment, Exam
from examcategories.models import ExamCategory
from senseis.models import Sensei


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
# EXAM ENROLLMENT
# -------------------------------
class ExamEnrollmentListView(LoginRequiredMixin, ListView):
    model = models.ExamEnrollment
    template_name = "enrollment_list.html"
    context_object_name = "enrollments"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        karateca = self.request.GET.get("karateca")
        if karateca:
            queryset = queryset.filter(karateca__name__icontains=karateca)
        return queryset


class ExamEnrollmentCreateView(LoginRequiredMixin, CreateView):
    model = models.ExamEnrollment
    template_name = "enrollment_create.html"
    form_class = forms.ExamEnrollmentForm
    success_url = reverse_lazy("enrollment_list")


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
# EXAM RESULT
# -------------------------------
from collections import OrderedDict
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from . import models


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
    

class ExamParticipantsByCategoryAPIView(generics.RetrieveAPIView):
    """
    Retorna os detalhes do exame + lista de participantes filtrados por categoria.
    """
    serializer_class = serializers.ExamSerializer  # ✅ usa o serializer completo

    def get_object(self):
        exam_id = self.kwargs.get("pk")
        category = self.kwargs.get("category")
        exam = get_object_or_404(models.Exam, id=exam_id)
        # ✅ filtra apenas os participantes da categoria informada
        exam.filtered_participants = models.ExamEnrollment.objects.filter(
            exam_id=exam_id,
            karateca__graduation__belt=category
        ).select_related("karateca", "exam")
        return exam

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["filtered_participants"] = getattr(self.get_object(), "filtered_participants", [])
        return context

