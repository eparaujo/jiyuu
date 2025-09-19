from django.db import models
from graduations.models import Graduation


class Sensei(models.Model):
    name  = models.CharField(max_length=200)
    cpf = models.CharField(max_length=15)
    graduation  = models.ForeignKey(Graduation, on_delete=models.DO_NOTHING, related_name='GraduacaoSensei', blank=True, null=True)
    email = models.CharField(max_length=150, blank=True, null=True)
    celPhone = models.CharField(max_length=60)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name 