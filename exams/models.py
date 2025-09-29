from django.db import models 
from dojos.models import Dojo
from karatecas.models import Karateca
from graduations.models import Graduation


# ======================================================
# Modelo principal que representa um Exame de Faixa
# ======================================================

STATUS_EXAM = [
    ('AGENDADO', 'Agendado'),
    ('CONFIRMADO', 'Confirmado'),
    ('CANCELADO', 'Cancelado'),
    ('FINALIZADO', 'Finalizado'),
]
class Exam(models.Model):
    """Exame de faixa em uma data específica"""

    # Um exame pertence a um dojo específico
    dojo = models.ForeignKey(Dojo, on_delete=models.CASCADE, related_name="exams")# permite acessar todos os exames com dojo.exams.all()
    date = models.DateField()  # Data marcada do exame
    description = models.TextField(blank=True, null=True)  # Descrição opcional do exame
    # Participantes são karatecas, mas o relacionamento é feito via tabela intermediária ExamEnrollment
    participants = models.ManyToManyField(Karateca,
        through="ExamEnrollment",       # Usa a tabela ExamEnrollment para guardar mais detalhes da inscrição
        related_name="exams"            # permite acessar todos os exames de um karateca com karateca.exams.all()
    )
    status = models.CharField(max_length=60, choices=STATUS_EXAM, blank=True, null=True)

    def __str__(self):
        # Exibição amigável no Django Admin e console
        return f"Exame em {self.date} - {self.dojo.tradename}"


# ======================================================
# Modelo que define as matérias avaliadas em um exame
# (Exemplo: kihon, kata, kumite)
# ======================================================
class ExamSubject(models.Model):
    """Matérias avaliadas em um exame (ex: kihon, kata...)"""
    name = models.CharField(max_length=100)  # Nome da matéria

    def __str__(self):
        return self.name


# ======================================================
# Modelo que define quais matérias (ExamSubject) 
# serão cobradas em determinado exame e suas notas mín/max
# ======================================================
class ExamRequirement(models.Model):
    """Matéria exigida em determinado exame"""

    # Relacionamento com o exame
    exam = models.ForeignKey(
        Exam,
        on_delete=models.CASCADE,
        related_name="requirements"  # exam.requirements.all() retorna todas exigências do exame
    )
    # Relacionamento com a matéria
    subject = models.ForeignKey(ExamSubject, on_delete=models.CASCADE)
    # Notas máxima e mínima para a matéria neste exame
    max_score = models.PositiveIntegerField(default=0)
    min_score = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.exam} - {self.subject}"


# ======================================================
# Modelo que guarda a inscrição de um karateca em um exame
# ======================================================
class ExamEnrollment(models.Model):
    """Inscrição de um karateca em um exame"""

    exam = models.ForeignKey(Exam,on_delete=models.CASCADE, related_name="enrollments")   # exam.enrollments.all() retorna todos inscritos

    karateca = models.ForeignKey(Karateca, on_delete=models.CASCADE,  related_name="exam_enrollments")# karateca.exam_enrollments.all() retorna todas inscrições do aluno

    current_graduation = models.ForeignKey(Graduation, on_delete=models.SET_NULL, null=True)   # se a graduação for apagada, mantém null

    # Marca se o aluno foi aprovado ou não no exame
    approved = models.BooleanField(
        default=False,
        help_text="Marca se o aluno foi aprovado no exame"
    )

    def __str__(self):
        return f"{self.karateca} inscrito no {self.exam}"


# ======================================================
# Modelo que armazena a nota do aluno em cada matéria
# ======================================================
class ExamResult(models.Model):
    """Nota de cada aluno em cada matéria"""

    # Inscrição do aluno (um aluno em um exame específico)
    enrollment = models.ForeignKey(ExamEnrollment, on_delete=models.CASCADE, related_name="results")   # enrollment.results.all() retorna todas as notas do aluno nesse exame
    
    # Matéria avaliada
    subject = models.ForeignKey(ExamSubject, on_delete=models.CASCADE)

    score = models.PositiveIntegerField()  # Nota obtida
    comments = models.TextField(max_length=250, blank=True, null=True)

    def __str__(self):
        return f"{self.enrollment.karateca} - {self.subject}: {self.score}"
