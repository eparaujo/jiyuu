from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self): 
        return self.name
 