from django.db import models
from karatecas.models import Karateca
from events.models import Event

class CourseEnrollment(models.Model):
    karateca = models.ForeignKey(Karateca, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, help_text='Curso ou Evento')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    billed = models.BooleanField(default=False)  # marca se já foi incluído no faturamento

    def __str__(self):
        return f"{self.karateca.name} - {self.event.name}"
