from django.db import models


class KarateStyle(models.Model):
    name = models.CharField(max_length=250)
    originstyle = models.CharField(max_length=150, null=True, blank=True)
    bases = models.CharField(max_length=150, null=True, blank=True)
    qtdekatas = models.IntegerField(null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name 