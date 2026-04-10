from django.db import models
from dojos.models import Dojo
from karatecas.models import Karateca
from graduations.models import Graduation
from senseis.models import Sensei
from examcategories.models import ExamCategory


# ======================================================
# Status possíveis do exame
# ======================================================
STATUS_EXAM = [
    ('AGENDADO', 'Agendado'),
    ('CONFIRMADO', 'Confirmado'),
    ('CANCELADO', 'Cancelado'),
    ('FINALIZADO', 'Finalizado'),
]


# ======================================================
# Modelo principal que representa um Exame de Faixa
# ======================================================
class Exam(models.Model):
    """Exame de faixa em uma data específica"""

    dojo = models.ForeignKey(Dojo, on_delete=models.CASCADE, related_name="exams")
    date = models.DateField()
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=60, choices=STATUS_EXAM, blank=True, null=True)

    # 🔹 Categorias de graduação que fazem parte deste exame
    categories = models.ManyToManyField(ExamCategory, related_name="exams", blank=True, help_text="Categorias de graduação que fazem parte do exame (ex: Branca -> Azul)" )

    # 🔹 Participantes (via tabela intermediária) 
    participants = models.ManyToManyField(
        Karateca,
        through="ExamEnrollment",
        related_name="exams"
    )

    def __str__(self):
        return f"Exame em {self.date} - {self.dojo.tradename}"


# ======================================================
# Matérias avaliadas no exame
# ======================================================
class ExamSubject(models.Model):
    """Matérias avaliadas em um exame (ex: kihon, kata...)"""
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# ======================================================
# Requisitos de cada exame (disciplinas + notas mínimas/máximas)
# ======================================================
class ExamRequirement(models.Model):
    """Matéria exigida em determinado exame"""

    exam = models.ForeignKey(
        Exam,
        on_delete=models.CASCADE,
        related_name="requirements"
    )
    category = models.ForeignKey(
        ExamCategory,
        on_delete=models.CASCADE,
        related_name="requirements"
    )
    subject = models.ForeignKey(ExamSubject, on_delete=models.CASCADE)
    max_score = models.DecimalField(max_digits=5, decimal_places=2)
    min_score = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        unique_together = ("exam", "category", "subject")

    def __str__(self):
        return f"{self.exam} - {self.subject}"


# ======================================================
# Inscrição de Karatecas em exames (por categoria)
# ======================================================
class ExamEnrollment(models.Model):
    """Inscrição de um karateca em um exame"""

    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name="enrollments")
    karateca = models.ForeignKey(Karateca, on_delete=models.CASCADE, related_name="exam_enrollments")
    current_graduation = models.ForeignKey(Graduation, on_delete=models.SET_NULL, null=True)
    # 🔹 Categoria do exame na qual o karateca está inscrito
    category = models.ForeignKey(ExamCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name="enrollments")
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.karateca} inscrito no {self.exam}"


# ======================================================
# Resultado e nota de cada aluno por matéria
# ======================================================
class ExamResult(models.Model):
    """Nota de cada aluno em cada matéria"""

    enrollment = models.ForeignKey(
        ExamEnrollment,
        on_delete=models.CASCADE,
        related_name="results"
    )
    subject = models.ForeignKey(ExamSubject, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    comments = models.TextField(max_length=250, blank=True, null=True)
    sensei_examiner = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return f"{self.enrollment.karateca} - {self.subject}: {self.score}"
