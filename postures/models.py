from django.db import models
from karatestyles.models import KarateStyle


class Posture(models.Model):
    name = models.CharField(max_length=300)
    style = models.ForeignKey(KarateStyle, on_delete=models.PROTECT, related_name='style')
    description = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to='movimentos/', blank=True, null=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name