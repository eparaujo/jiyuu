from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from . import models, forms
from rest_framework import generics
from .serializers import TechnicalProgramItemSerializer, TechnicalProgramSerializer

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from graduations.models import Graduation
from examcategories.models import ExamCategory


# Create your views here.
class TechnicalProgramCreateView(LoginRequiredMixin, CreateView):
    model = models.TechnicalProgram
    form_class = forms.TechnicalProgramForm
    template_name = "technical_program_create.html"
    success_url = reverse_lazy(
        "technical_program_list"
    )


class TechnicalProgramListView(LoginRequiredMixin, ListView):
    model = models.TechnicalProgram
    template_name = "technical_program_list.html"
    context_object_name = "programs"

    def get_queryset(self):
        return (
            models.TechnicalProgram.objects
            .select_related(
                "category",
                "category__to_graduation",
            )
            .prefetch_related("items")
            .order_by(
                "category__to_graduation__order",
                "category__to_graduation__id",
            )
        )

class TechnicalProgramUpdateView(LoginRequiredMixin, UpdateView):
    model = models.TechnicalProgram
    form_class = forms.TechnicalProgramForm
    template_name = "technical_program_update.html"
    success_url = reverse_lazy(
        "technical_program_list"
    )

class TechnicalProgramDeleteView(LoginRequiredMixin, DeleteView):
    model = models.TechnicalProgram
    template_name = "technical_program_delete.html"
    success_url = reverse_lazy(
        "technical_program_list"
    )

class TechnicalProgramDetailView(LoginRequiredMixin, DetailView):
    model = models.TechnicalProgram
    template_name = "technical_program_detail.html"
    context_object_name = "program"

    def get_queryset(self):
        return (
            models.TechnicalProgram.objects
            .select_related("category")
            .prefetch_related("items")
        )

# -------------------------------------------------------
# Views - TechnicalProgramItem
# -------------------------------------------------------

class TechnicalProgramItemCreateView(LoginRequiredMixin, CreateView):
    model = models.TechnicalProgramItem
    form_class = forms.TechnicalProgramItemForm
    template_name = "technical_program_item_create.html"
    success_url = reverse_lazy(
        "technical_program_item_list"
    )


class TechnicalProgramItemListView(LoginRequiredMixin, ListView):
    model = models.TechnicalProgramItem
    template_name = "technical_program_item_list.html"
    context_object_name = "items"

    def get_queryset(self):
        queryset = (
            models.TechnicalProgramItem.objects
            .select_related(
                "program",
                "program__category",
            )
            .order_by(
                "program__category__name_category",
                "modality",
                "sequence",
            )
        )

        title = self.request.GET.get("title")

        if title:
            queryset = queryset.filter(
                title__icontains=title
            )

        return queryset


class TechnicalProgramItemDetailView(LoginRequiredMixin, DetailView):
    model = models.TechnicalProgramItem
    template_name = "technical_program_item_detail.html"
    context_object_name = "item"

    def get_queryset(self):
        return (
            models.TechnicalProgramItem.objects
            .select_related(
                "program",
                "program__category",
            )
        )


class TechnicalProgramItemUpdateView(LoginRequiredMixin, UpdateView):
    model = models.TechnicalProgramItem
    form_class = forms.TechnicalProgramItemForm
    template_name = "technical_program_item_update.html"
    success_url = reverse_lazy(
        "technical_program_item_list"
    )

    def get_queryset(self):
        return (
            models.TechnicalProgramItem.objects
            .select_related(
                "program",
                "program__category",
            )
        )


class TechnicalProgramItemDeleteView(LoginRequiredMixin, DeleteView):
    model = models.TechnicalProgramItem
    template_name = "technical_program_item_delete.html"
    success_url = reverse_lazy(
        "technical_program_item_list"
    )

    def get_queryset(self):
        return (
            models.TechnicalProgramItem.objects
            .select_related(
                "program",
                "program__category",
            )
        )                 
#-------------------------------------------------------                
# View a serem usadas pelos endpoints do flutter
#-------------------------------------------------------
class TechnicalProgramListAPIView(
    generics.ListAPIView
):
    queryset = (
        models.TechnicalProgram.objects
        .select_related("category")
        .prefetch_related("items")
        .filter(active=True)
    )

    serializer_class = TechnicalProgramSerializer

class TechnicalProgramDetailAPIView(
    generics.RetrieveAPIView
):
    queryset = (
        models.TechnicalProgram.objects
        .select_related("category")
        .prefetch_related("items")
        .filter(active=True)
    )

    serializer_class = TechnicalProgramSerializer

# --------------------------------------------------
# View a ser utilizada pelo Ap para buscar o programa técnico
# --------------------------------------------------
class TechnicalProgramNextAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        # --------------------------------------------------
        # Karateca autenticado
        # --------------------------------------------------
        karateca = request.user.karateka

        if not karateca or not karateca.graduation:
            return Response(
                {
                    "detail": "Graduação do karateca não encontrada."
                },
                status=404
            )

        # --------------------------------------------------
        # Graduação atual
        # --------------------------------------------------
        current_graduation = karateca.graduation

        # --------------------------------------------------
        # Próxima graduação
        # Usa a mesma regra do status de graduação
        # --------------------------------------------------
        next_graduation = (
            Graduation.objects
            .filter(
                order__gt=current_graduation.order
            )
            .order_by("order")
            .first()
        )

        if not next_graduation:
            return Response(
                {
                    "detail": "Não existe próxima graduação."
                },
                status=404
            )

        # --------------------------------------------------
        # Categoria correspondente à próxima graduação
        # --------------------------------------------------
        category = (
            ExamCategory.objects
            .filter(
                to_graduation=next_graduation,
                technical_program__active=True,
            )
            .select_related("to_graduation")
            .first()
        )

        if not category:
            return Response(
                {
                    "detail": (
                        "Não existe programa técnico "
                        "cadastrado para a próxima graduação."
                    ),
                    "next_graduation": next_graduation.name,
                },
                status=404
            )

        # --------------------------------------------------
        # Programa técnico
        # --------------------------------------------------
        program = (
            models.TechnicalProgram.objects
            .select_related(
                "category",
                "category__to_graduation",
            )
            .prefetch_related("items")
            .filter(
                category=category,
                active=True,
            )
            .first()
        )

        if not program:
            return Response(
                {
                    "detail": (
                        "Não existe programa técnico "
                        "cadastrado para a próxima graduação."
                    ),
                    "next_graduation": next_graduation.name,
                    "category": category.name_category,
                },
                status=404
            )

        # --------------------------------------------------
        # Serialização
        # --------------------------------------------------
        serializer = TechnicalProgramSerializer(program)        

        return Response(serializer.data)