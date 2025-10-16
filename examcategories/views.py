from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from . import models, forms
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from . import serializers
from rest_framework import generics


class ExamCategoryListView(LoginRequiredMixin, ListView):
    model = models.ExamCategory
    template_name = 'examcategory_list.html'
    context_object_name ='examcategories'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        name_category = self.request.GET.get('name_category')
        
        if name_category:
            queryset = queryset.filter(name_category__icontains=name_category)
        return queryset
    
class ExamCategoryCreateView(LoginRequiredMixin, CreateView):
    model = models.ExamCategory
    template_name = 'examcategory_create.html'
    form_class = forms.ExamCategoryForm
    success_url = reverse_lazy('examcategory_list')

class ExamCategoryDetailView(LoginRequiredMixin, DeleteView):
    model = models.ExamCategory
    template_name = 'examcategory_detail.html'

class ExamCategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = models.ExamCategory
    template_name = 'examcategory_update.html'
    form_class = forms.ExamCategoryForm
    success_url = reverse_lazy('examcategory_list')    

class ExamCategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = models.ExamCategory
    template_name = 'examcategory_delete.html'
    success_url = reverse_lazy('examcategory_list')

# views exclusivas para serem usadas via api externa
class ExamCategoryListAPIView(generics.ListCreateAPIView):
    queryset = models.ExamCategory.objects.all()
    serializer_class = serializers.ExamCategoriesSerializers

class ExamCategoryRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.ExamCategory.objects.all()
    serializer_class = serializers.ExamCategoriesSerializers