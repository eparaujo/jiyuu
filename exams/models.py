from django.db import models
from dojos.models import Dojo
from karatecas.models import Karateca
from graduations.models import Graduation


class Exam(models.Model):
    """Exame de faixa em uma data específica"""
    dojo = models.ForeignKey(Dojo, on_delete=models.CASCADE, related_name="exams")  # permite acessar exams pelo dojo.exams.all()
    
    date = models.DateField()  # data do exame
    description = models.TextField(blank=True, null=True)

    # Participantes através da tabela de inscrição
    participants = models.ManyToManyField( Karateca, through="ExamEnrollment", related_name="exams")  # ligação via inscrição

    def __str__(self):
        return f"Exame em {self.date} - {self.dojo.tradename}"


class ExamSubject(models.Model):
    """Matérias avaliadas em um exame (ex: kihon, kata...)"""
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ExamRequirement(models.Model):
    """Matéria exigida em determinado exame"""
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name="requirements")
    subject = models.ForeignKey(ExamSubject, on_delete=models.CASCADE)
    max_score = models.PositiveIntegerField(default=0)
    min_score = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.exam} - {self.subject}"


class ExamEnrollment(models.Model):
    """Inscrição de um karateca em um exame"""
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name="enrollments")
    karateca = models.ForeignKey(Karateca, on_delete=models.CASCADE, related_name="exam_enrollments")
    current_graduation = models.ForeignKey(Graduation, on_delete=models.SET_NULL, null=True)
    approved = models.BooleanField(default=False, help_text="Marca se o aluno foi aprovado no exame") # indica verdadeiro ou falso para aprovado ou reprovado

    def __str__(self):
        return f"{self.karateca} inscrito no {self.exam}"


class ExamResult(models.Model):
    """Nota de cada aluno em cada matéria"""
    enrollment = models.ForeignKey(ExamEnrollment, on_delete=models.CASCADE, related_name="results")
    subject = models.ForeignKey(ExamSubject, on_delete=models.CASCADE)
    score = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.enrollment.karateca} - {self.subject}: {self.score}"
