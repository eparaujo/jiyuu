from django.db import models
from graduations.models import Graduation
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Event(models.Model):
    KIND_EVENT = [
        ('EXAME', 'Exame de Faixa'),
        ('TREINO', 'Treinamento Especial'),
        ('CAMPEONATO', 'Campeonato'),
        ('SEMINARIO', 'Seminário'),
        ('OUTRO', 'Outro'),
    ]
    
    LEVEL_EVENT = [
        ('INTERNO', 'Interno (Clube/Dojô)'),
        ('MUNICIPAL', 'Municipal'),
        ('REGIONAL', 'Regional'),
        ('ESTADUAL', 'Estadual'),
        ('NACIONAL', 'Nacional'),
        ('INTERNACIONAL', 'Internacional'),
        ('FESTIVO', 'Festivo/Exibição'),
    ]

    CATEGORY = [
        ('INFANTIL', 'Infantil'),
        ('JUVENIL', 'Juvenil'),
        ('ADULTO', 'Adulto'),
        ('MASTER', 'Master'),
    ]

    MODALITY = [
        ('KATA', 'Kata'),
        ('KUMITE', 'Kumite'),
        ('KATATEAM', "Kata Equipe"),
        ('KUMITETEAM', 'Kumite Equipe'),
    ]

    STATUS = [
        ('PENDENTE', 'Pendente'),
        ('CONFIRMADA', 'Confirmada'),
        ('CANCELADA', 'Cancelada'),
        ('OUTROS', 'Outros'),
    ]

    name = models.CharField(max_length=150)
    kind = models.CharField(max_length=20, choices=KIND_EVENT)
    level = models.CharField(max_length=20, choices=LEVEL_EVENT)
    date = models.DateField()
    start_time = models.TimeField(null=True, blank=True)
    end_time =models.TimeField(null=True, blank=True)
    local = models.CharField(max_length=300)
    adress = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    # faixas habilitadas para o exame
    hability_graduation = models.ForeignKey(Graduation, on_delete=models.DO_NOTHING, related_name='event_graduation')

    #para campeonatos
    category = models.CharField(max_length=30, choices=CATEGORY)
    modalitiy = models.CharField(max_length=30, choices=MODALITY)

    #dados da inscrição
    registration_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    limite_date = models.DateField(null=True, blank=True)
    
    organizer = models.CharField(max_length=150, blank=True, null=True) # entidade organizadora do evento (FPK, CBK, etc.)
    event_organizer = models.CharField(max_length=200, blank=True, null=True) # pessoal responsável por cadastrar dados do evento

    status = models.CharField(max_length=60, choices=STATUS, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name} - {self.get_kind_display()} - {self.date}'
