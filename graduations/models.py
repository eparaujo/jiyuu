from django.db import models


class Graduation(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name 