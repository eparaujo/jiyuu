from django.db import models
from dojos.models import Dojo
from karatecas.models import Karateca
import secrets
from django.utils import timezone
from datetime import timedelta
from classes.models import Aula


class TrainingAttendance(models.Model):
    """
    Registro de presença/falta em treinamentos.
    """

    karateca = models.ForeignKey(
        Karateca,
        on_delete=models.CASCADE,
        related_name="training_attendances"
    )

    dojo = models.ForeignKey(
        Dojo,
        on_delete=models.CASCADE,
        related_name="training_attendances"
    )

    aula = models.ForeignKey(
        "classes.Aula",
        on_delete=models.CASCADE,
         related_name="training_attendances",
        null=True,
        blank=True
    )

    training_date = models.DateField()

    present = models.BooleanField(
        default=True,
        help_text="True = presente | False = falta"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        verbose_name = "Training Attendance"
        verbose_name_plural = "Training Attendances"

        unique_together = (
            "karateca",
            "aula",
            "training_date"
        )

        ordering = ["-training_date"]

    def __str__(self):

        status = (
            "Presente"
            if self.present
            else "Falta"
        )

        return (
            f"{self.karateca} - "
            f"{self.aula.name} - "
            f"{self.training_date} ({status})"
        )
    
#------------------------------------------
#Model para geração de token e QR Code, onde
#o aluno vai registrar presença
#------------------------------------------
class TrainingCheckinSession(models.Model):

    aula = models.ForeignKey(
        "classes.Aula",
        on_delete=models.CASCADE,
        related_name="checkin_sessions"
    )

    dojo = models.ForeignKey(
        Dojo,
        on_delete=models.CASCADE,
        related_name="checkin_sessions"
    )

    created_by = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE
    )

    token = models.CharField(
        max_length=255,
        unique=True
    )

    is_active = models.BooleanField(
        default=True
    )

    expires_at = models.DateTimeField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):

        if not self.token:
            self.token = secrets.token_urlsafe(32)

        if not self.expires_at:

            self.expires_at = (
                timezone.now() + timedelta(minutes=5)
            )

        super().save(*args, **kwargs)

    def is_valid(self):

        return (
            self.is_active and
            timezone.now() <= self.expires_at
        )

    def __str__(self):

        return (
            f"{self.aula.name} - QR Session"
        )