from django.db import models
from graduations.models import Graduation
from dojos.models import Dojo
from genres.models import Genre
from revenues.models import Revenue

class Karateca(models.Model):

    STATUS = [
        ('ATIVO', 'Ativo'),
        ('AFASTADO', 'Afastado'),
        ('LICENCIADO', 'Licenciado'),
        ('CANCELADO', 'Desmatriculado'),
    ]

    name = models.CharField(max_length=200)
    genre = models.ForeignKey(Genre, on_delete=models.PROTECT, related_name='genres')
    cpf = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(unique=True)
    celphone = models.CharField(max_length=60, blank=True, null=True)
    graduation = models.ForeignKey(Graduation, on_delete=models.PROTECT, related_name='graduation', blank=True, null=True)
    dojo = models.ForeignKey(Dojo, on_delete=models.PROTECT,related_name='dojo')
    monthlypay =  models.ForeignKey(Revenue, on_delete=models.PROTECT, related_name='mensalidade')
    active = models.CharField(max_length=60, choices=STATUS, blank=True, null=True) #alunos com status igual a ATIVO
    total_karatecas = models.IntegerField(blank=True, null=True)

    class Meta:
        ordering = ['name']


    def __str__(self):
        return self.name