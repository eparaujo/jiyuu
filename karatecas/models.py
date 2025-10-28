from django.db import models
from django.contrib.auth.models import User  # 🔹 Import necessário para o relacionamento com usuário
from graduations.models import Graduation
from dojos.models import Dojo
from genres.models import Genre
from revenues.models import Revenue
from kindrevenues.models import KindRevenue


class Karateca(models.Model):
    """
    Modelo que representa um Karateca (aluno), com vínculo a um usuário Django.
    O usuário é criado automaticamente no momento do cadastro via API.
    """

    STATUS = [
        ('ATIVO', 'Ativo'),
        ('AFASTADO', 'Afastado'),
        ('LICENCIADO', 'Licenciado'),
        ('CANCELADO', 'Desmatriculado'),
    ]

    # 🔹 Relacionamento com o usuário Django
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='karateka')

    # 🔹 Dados principais
    name = models.CharField(max_length=200)
    genre = models.ForeignKey(Genre, on_delete=models.PROTECT,        related_name='karatekas')
    cpf = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(unique=True)
    celphone = models.CharField(max_length=60, blank=True, null=True)

    # 🔹 Graduação e faixa
    graduation = models.ForeignKey(Graduation, on_delete=models.PROTECT, related_name='karatekas', blank=True, null=True)
    dan = models.CharField(max_length=60, blank=True, null=True)  # 🔹 Grau (1º Dan, 2º Dan, etc.)

    # 🔹 Outras informações fixas
    dojo = models.ForeignKey(Dojo, on_delete=models.PROTECT, related_name='karatekas')
    #monthlypay = models.ForeignKey(KindRevenue, on_delete=models.PROTECT, related_name='mensalidade')
    active = models.CharField(max_length=60, choices=STATUS, default='ATIVO')# 🔹 Valor padrão
    monthly_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0) # valor da mensalidade
    due_day = models.PositiveSmallIntegerField(default=5)  # dia de vencimento da mensalidade (1-31)
  
    
    # 🔹 Campo adicional de controle
    #total_karatecas = models.IntegerField(blank=True, null=True)

    class Meta:
        ordering = ['name']
        verbose_name = "Karateca"
        verbose_name_plural = "Karatecas"

    def __str__(self):
        return self.name

    # 🔹 Método utilitário para criação de usuário vinculado
    def create_user_account(self, password):
        """
        Cria e vincula automaticamente um usuário Django
        para o Karateca recém-cadastrado.
        """
        if not self.user:
            username = self.email  # usamos o e-mail como username
            user = User.objects.create_user(
                username=username,
                email=self.email,
                password=password
            )
            self.user = user
            self.save()
