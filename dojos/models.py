from django.db import models
from classes.models import Aula
from senseis.models import Sensei
from expenses.models import Expense
from revenues.models import Revenue


# Create your models here.
class Dojo(models.Model):
    razaosocial = models.CharField(max_length=200)
    tradename = models.CharField(max_length=200, blank=True, null=True)
    site = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=200, unique=True)
    whatsapp = models.CharField(max_length=60, blank=True, null=True)
    phone = models.CharField(max_length=60, blank=True, null=True)
    street = models.CharField(max_length=200, blank=True, null=True)
    number = models.IntegerField()
    zipcode = models.CharField(max_length=20, blank=True, null=True)
    district = models.CharField(max_length=160, blank=True, null=True)
    city = models.CharField(max_length=160, blank=True, null=True)
    state = models.CharField(max_length=160, blank=True, null=True)
    country = models.CharField(max_length=160, blank=True, null=True)
    aulas = models.ManyToManyField(Aula, related_name='auladojo')
    sensei = models.ManyToManyField(Sensei, related_name='sensei') #sensei responsável pelo Dojo
    revenues = models.ManyToManyField(Revenue, related_name='receitas')
    expenses = models.ManyToManyField(Expense, related_name='despesas')

    class Meta:
        ordering = ['tradename']
 
    def __str__(self):
        return self.tradename