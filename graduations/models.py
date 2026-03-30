from django.db import models


class Graduation(models.Model):
    name = models.CharField(max_length=100)
    order = models.PositiveSmallIntegerField(default=0)  #campo a ser usado futuramente pelo sensei ou adm, saber qual a próxima graduação, exemplo de branca para azul
    min_months = models.PositiveSmallIntegerField(
        default=6,
        help_text="Meses mínimos de carência para próximo exame"
    )

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name 