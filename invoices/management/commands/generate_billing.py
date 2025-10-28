from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from karatecas.models import Karateca
from invoices.models import Invoice
from invoiceItem.models import InvoiceItem
from events.models import Event

class Command(BaseCommand):
    help = 'Gera faturas mensais de todos os karatecas ativos'

    def handle(self, *args, **options):
        today = timezone.now().date()
        karatecas = Karateca.objects.filter(active=True)

        for karateca in karatecas:
            due_day = karateca.due_day or 10  # dia padrão de vencimento
            due_date = today.replace(day=due_day) if today.day <= due_day else (today + timedelta(days=30)).replace(day=due_day)

            # cria a fatura
            invoice = Invoice.objects.create(
                karateca=karateca,
                issue_date=today,
                due_date=due_date,
            )

            # adiciona a mensalidade
            InvoiceItem.objects.create(
                invoice=invoice,
                item_type='MONTHLY_FEE',
                description=f'Mensalidade de {today.strftime("%B/%Y")}',
                amount=karateca.monthly_fee,
            )

            # adiciona eventos do mês corrente
            events = Event.objects.filter(participants=karateca, date__month=today.month, date__year=today.year)
            for event in events:
                InvoiceItem.objects.create(
                    invoice=invoice,
                    item_type='EVENT',
                    description=event.name,
                    amount=event.price,
                    event=event
                )

            invoice.calculate_total()
            self.stdout.write(self.style.SUCCESS(f'Fatura criada para {karateca} (R$ {invoice.total_amount})'))

        self.stdout.write(self.style.SUCCESS('Faturamento mensal concluído!'))
