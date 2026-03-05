from django.db import models
from dojos.models import Dojo
from karatecas.models import Karateca


class TrainingAttendance(models.Model):
    """
    Registro de presença/falta em treinamentos.
    Totalmente independente de exames.
    """

    karateca = models.ForeignKey(Karateca, on_delete=models.CASCADE, related_name="training_attendances")

    dojo = models.ForeignKey(Dojo, on_delete=models.CASCADE, related_name="training_attendances")

    training_date = models.DateField()

    present = models.BooleanField(default=True, help_text="True = presente | False = falta")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Training Attendance"
        verbose_name_plural = "Training Attendances"
        unique_together = ("karateca", "dojo", "training_date")
        ordering = ["-training_date"]

    def __str__(self):
        status = "Presente" if self.present else "Falta"
        return f"{self.karateca} - {self.training_date} ({status})"