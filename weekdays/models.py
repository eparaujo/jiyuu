from django.db import models


class Weekday(models.Model):
    dayname = models.CharField(max_length=50)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.dayname 