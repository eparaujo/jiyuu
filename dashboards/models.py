from django.db import models
from dojos.models import Dojo
from events.models import Event

class Dashboard(models.Model):
    dojo = models.ForeignKey(Dojo, on_delete=models.CASCADE, related_name="dashboard")

    # Estatísticas de alunos
    active_students = models.IntegerField(default=0) # número de karatecas com status igual a Ativo

    # Último exame
    last_exam_date = models.DateField(null=True, blank=True)
    last_exam_participants = models.IntegerField(default=0) #Número de participantes
    last_exam_approved = models.IntegerField(default=0) # Número de aprovados
    last_exam_students = models.JSONField(default=list, blank=True) # lista de karatecas participantes

    # Próximo exame
    next_exam_date = models.DateField(null=True, blank=True)
    next_exam_registered = models.IntegerField(default=0) # número de inscritos
    next_exam_students = models.JSONField(default=list, blank=True) #lista de karatecas participantes
    next_exam_name = models.CharField(max_length=255, blank=True) # Data do próximo exame

    # Lita Eventos futuros
    upcoming_events = models.JSONField(default=list, blank=True)
    #data de atualização
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Dashboard - {self.dojo.tradename or self.dojo.razaosocial}"

    @property
    def sensei(self):
        """Retorna o sensei vinculado ao dojo"""
        return self.dojo.sensei
