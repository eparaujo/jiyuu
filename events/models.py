from django.db import models
from karatecas.models import Karateca
from graduations.models import Graduation


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Modality(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Event(models.Model):
    KIND_CHOICES = [
        ('Curso', 'Curso'),
        ('Treino Especial', 'Treino Especial'),
        ('Campeonato', 'Campeonato'),
        ('Outros', 'Outros'),
    ]

    LEVEL_CHOICES = [
        ('Regional', 'Regional'),
        ('Estadual', 'Estadual'),
        ('Nacional', 'Nacional'),
        ('Internacional', 'Internacional'),
    ]

    STATUS_CHOICES = [
        ('Aberto', 'Aberto'),
        ('Encerrado', 'Encerrado'),
        ('Cancelado', 'Cancelado'),
    ]

    name = models.CharField(max_length=100)
    kind = models.CharField(max_length=30, choices=KIND_CHOICES)
    level = models.CharField(max_length=30, choices=LEVEL_CHOICES)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    local = models.CharField(max_length=100)
    address = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True)

    hability_graduation = models.ManyToManyField(Graduation, blank=True)
    category = models.ManyToManyField(Category, blank=True)
    modality = models.ManyToManyField(Modality, blank=True)

    registration_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    limite_date = models.DateField()
    organizer = models.CharField(max_length=100)
    event_organizer = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Aberto")

    participants = models.ManyToManyField(
        Karateca,
        through="CourseEnrollment",
        related_name="event_participations",
        blank=True
    )

    def __str__(self):
        return self.name


class CourseEnrollment(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    karateca = models.ForeignKey(Karateca, on_delete=models.CASCADE)
    enrollment_date = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)

    class Meta:
        unique_together = ('event', 'karateca')

    def __str__(self):
        return f"{self.karateca.name} - {self.event.name}"
