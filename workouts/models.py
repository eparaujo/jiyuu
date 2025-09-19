from django.db import models
from karatestyles.models import KarateStyle


class Workout(models.Model):
    name = models.CharField(max_length=200)
    style = models.ForeignKey(KarateStyle, on_delete=models.PROTECT, related_name='workouts')
    description = models.TextField(null=True, blank=True)
    movie_workout = models.FileField(upload_to='workout/', blank=True, null=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name 