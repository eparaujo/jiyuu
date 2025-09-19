# exams/views.py
from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from . import models, forms


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
class ExamResultListView(LoginRequiredMixin, ListView):
    model = models.ExamResult
    template_name = "result_list.html"
    context_object_name = "results"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        subject = self.request.GET.get("subject")
        if subject:
            queryset = queryset.filter(subject__name__icontains=subject)
        return queryset


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
