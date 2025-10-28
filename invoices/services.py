from django.utils import timezone
from datetime import date
from decimal import Decimal
from billingCycle.models import BillingCycle
from invoices.models import Invoice
from invoiceItem.models import InvoiceItem
from karatecas.models import Karateca
from courseEnrollment.models import CourseEnrollment

def generate_monthly_billing():
    """
    Gera automaticamente as faturas de todos os karatecas ativos
    no início de cada mês, incluindo mensalidades e cursos/eventos inscritos.
    """
    today = timezone.now().date()
    month = today.month
    year = today.year

    # Cria ou recupera o ciclo de faturamento
    billing_cycle, _ = BillingCycle.objects.get_or_create(month=month, year=year)

    # Varre todos os karatecas ativos
    for k in Karateca.objects.filter(active=True):
        due_date = date(year, month, min(k.due_day, 28))

        # Cria fatura se ainda não existir
        invoice, created = Invoice.objects.get_or_create(
            karateca=k,
            billing_cycle=billing_cycle,
            defaults={"due_date": due_date}
        )

        # Adiciona a mensalidade
        if created:
            InvoiceItem.objects.create(
                invoice=invoice,
                description="Mensalidade",
                amount=k.monthly_fee,
                item_type="MONTHLY",
                due_date=due_date
            )

        # Inclui cursos/eventos do mês
        enrollments = CourseEnrollment.objects.filter(
            karateca=k,
            billed=False,
            course__date__month=month,
            course__date__year=year
        )

        for e in enrollments:
            InvoiceItem.objects.create(
                invoice=invoice,
                description=f"Curso: {e.course.title}",
                amount=e.course.value,
                item_type="COURSE",
                due_date=due_date
            )
            e.billed = True
            e.save()

        # Atualiza o total
        total = sum(item.amount for item in invoice.invoiceitem_set.all())
        invoice.total_amount = Decimal(total)
        invoice.save()

    print(f"Faturamento de {month:02d}/{year} gerado com sucesso.")
