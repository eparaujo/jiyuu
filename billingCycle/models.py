from django.db import models
from datetime import date
import calendar

class BillingCycle(models.Model):
    month = models.PositiveSmallIntegerField()  # 1–12
    year = models.PositiveSmallIntegerField()
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    closed = models.BooleanField(default=False)
    closed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('month', 'year')
        ordering = ['-year', '-month']

    def __str__(self):
        return f"{self.month:02d}/{self.year}"

    def save(self, *args, **kwargs):
        """Define start_date e end_date automaticamente, se não informados."""
        if not self.start_date or not self.end_date:
            start = date(self.year, self.month, 1)
            last_day = calendar.monthrange(self.year, self.month)[1]
            end = date(self.year, self.month, last_day)
            self.start_date = start
            self.end_date = end
        super().save(*args, **kwargs)

    # === Métodos de controle de ciclo ===
    def close_cycle(self):
        """Fecha o ciclo, impedindo novas faturas."""
        if not self.closed:
            from django.utils import timezone
            self.closed = True
            self.closed_at = timezone.now()
            self.save()

    def reset_cycle(self, confirm=False):
        """
        Apaga todas as faturas vinculadas ao ciclo.
        'confirm=True' precisa ser passado explicitamente.
        """
        if not confirm:
            raise ValueError("Confirmação obrigatória: use reset_cycle(confirm=True).")

        from invoices.models import Invoice  # import local para evitar circular import
        deleted_count, _ = Invoice.objects.filter(billing_cycle=self).delete()
        self.closed = False
        self.closed_at = None
        self.save()
        return deleted_count
