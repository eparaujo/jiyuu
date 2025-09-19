from django.db.models.query import QuerySet
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from . import models, forms, serializers
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from rest_framework import generics


class EventListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = models.Event
    template_name = 'event_list.html'
    context_object_name = 'events'
    paginate_by = 10
    permission_required = 'events_view_event'

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get('name')

        if name:
            queryset = queryset.filter(name__icontains=name)

        return queryset
    
class EventCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = models.Event
    template_name = 'event_create.html'
    form_class = forms.EventForm
    success_url = reverse_lazy('event_list')
    permission_required = 'events.add.event'

class EventDetailView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = models.Event
    template_name = 'event_detail.html'
    EventDetailView = 'events.view_event'
    permission_required = 'events.view_event'

class EventUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView)    :
    model = models.Event
    template_name = 'event_update.html'
    form_class = forms.EventForm
    success_url = reverse_lazy('event_list')
    permission_required = 'events.change_event'

class EventDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = models.Event
    template_name = 'event_delete.html'
    success_url = reverse_lazy('event_list')
    permission_required = 'events.delete_event'