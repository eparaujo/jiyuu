from django.db import models
from weekdays.models import Weekday
from senseis.models import Sensei


class Aula(models.Model):
    name = models.CharField(max_length=200)
    day = models.ForeignKey(Weekday, on_delete=models.PROTECT, related_name='aulas')
    start = models.TimeField()
    end = models.TimeField()
    sensei = models.ForeignKey(Sensei, on_delete=models.PROTECT, related_name='senseis')
    description = models.TextField(blank=True, null=True)


    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name  