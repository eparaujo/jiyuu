from django.db import models
from karatestyles.models import KarateStyle


class Kata(models.Model):
    namekata = models.CharField(max_length=100)
    style = models.ForeignKey(KarateStyle, on_delete=models.PROTECT, related_name='styles')
    qtde_moviments = models.IntegerField()
    file = models.FileField(upload_to='videos/', blank=True, null=True)
    link = models.URLField(max_length=300, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['namekata']

    def __str__(self):
        return self.namekata 