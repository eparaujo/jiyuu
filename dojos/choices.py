from django.db import models

class DojoRole(models.TextChoices):
    OWNER = 'OWNER', 'Sensei Responsável'
    ADMIN = 'ADMIN', 'Administrador'
    STUDENT = 'STUDENT', 'Aluno'
