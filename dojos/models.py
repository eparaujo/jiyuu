from django.db import models
from classes.models import Aula
from senseis.models import Sensei
from expenses.models import Expense
from revenues.models import Revenue
from dojos.choices import DojoRole
from django.contrib.auth.models import User


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
    
 #class view usada para perfís de acesso   
class DojoMembership(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='dojo_memberships'
    )
    dojo = models.ForeignKey(
        'Dojo',
        on_delete=models.CASCADE,
        related_name='memberships'
    )
    role = models.CharField(
        max_length=20,
        choices=DojoRole.choices,
        default=DojoRole.STUDENT
    )
    is_active = models.BooleanField(default=True)        # utilizado para "deletar", porém apenas inativa o aluno/atleta
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'dojo')
        verbose_name = 'Vínculo com Dojo'
        verbose_name_plural = 'Vínculos com Dojo'

    def __str__(self):
        return f"{self.user.username} - {self.dojo.tradename} ({self.role})"