from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from rest_framework import generics
from .models import CourseEnrollment
from events.models import Event
from .forms import EventForm
from .serializers import EventSerializer, CourseEnrollmentSerializer
from karatecas.models import Karateca


# ------------------------------ HTML Views ------------------------------

class EventListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Event
    template_name = "event_list.html"
    context_object_name = "events"
    paginate_by = 10
    permission_required = "events.view_event"

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get("name")
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset


class EventCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Event
    template_name = "event_create.html"
    form_class = EventForm
    success_url = reverse_lazy("event_list")
    permission_required = "events.add_event"


class EventDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Event
    template_name = "event_detail.html"
    permission_required = "events.view_event"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = self.object
        context["enrollments"] = CourseEnrollment.objects.filter(event=event).select_related("karateca")
        return context


class EventUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Event
    template_name = "event_update.html"
    form_class = EventForm
    success_url = reverse_lazy("event_list")
    permission_required = "events.change_event"


class EventDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Event
    template_name = "event_delete.html"
    success_url = reverse_lazy("event_list")
    permission_required = "events.delete_event"

# ------------------------------ Inscrição de Karateca na tela------------------------------
def EventEnrollmentFormView(request):
    """
    View para inscrever um karateca em um evento.
    """
    #events = Event.objects.filter(status="Aberto")
    events = Event.objects.all()
    karatecas = Karateca.objects.all()

    if request.method == "POST":
        event_id = request.POST.get("event_id")
        karateca_id = request.POST.get("karateca_id")

        if not event_id or not karateca_id:
            messages.error(request, "Selecione o evento e o karateca.")
            return redirect("event_enrollment_form")

        event = get_object_or_404(Event, id=event_id)
        karateca = get_object_or_404(Karateca, id=karateca_id)

        # Evita inscrições duplicadas
        if CourseEnrollment.objects.filter(event=event, karateca=karateca).exists():
            messages.warning(request, f"{karateca.name} já está inscrito neste evento.")
        else:
            CourseEnrollment.objects.create(event=event, karateca=karateca)
            messages.success(request, f"{karateca.name} inscrito com sucesso no evento {event.name}.")

        return redirect("event_list")

    return render(
        request,
        "event_enrollment.html",
        {"events": events, "karatecas": karatecas}
    )


def toggle_payment_status(request, enrollment_id):
    enrollment = get_object_or_404(CourseEnrollment, pk=enrollment_id)
    enrollment.paid = not enrollment.paid
    enrollment.save()
    messages.success(request, f"Status de pagamento atualizado para {'Pago' if enrollment.paid else 'Pendente'}.")
    return redirect("event_detail", pk=enrollment.event.id)


# ------------------------------ API Views ------------------------------

class EventListAPI(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class CourseEnrollmentCreateAPI(generics.CreateAPIView):
    queryset = CourseEnrollment.objects.all()
    serializer_class = CourseEnrollmentSerializer
