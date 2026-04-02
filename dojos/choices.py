from django.db import models

class DojoRole(models.TextChoices):
    OWNER = 'OWNER', 'Sensei Responsável'
    ADMIN = 'ADMIN', 'Administrador'
    EXAMINER = "EXAMINER", "Examinador"
    STUDENT = 'STUDENT', 'Aluno'
    SENSEI = 'SENSEI', 'Sensei' 