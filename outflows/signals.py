from django.db.models.signals import post_save
from django.dispatch import receiver # fica escutando e quando ocorrer um post_save, ele executa
from expenses.models import Expense
from outflows.models import Outflow

@receiver(post_save, sender=Outflow) #aqui estamos falando que sempre que houver um post_save em Revenue, esta função será executada
def update_expense(sender, instance, created, **kwargs):
    if created:
        if instance.value > 0:
            expense = instance.expense
            expense.value += instance.value
            expense.save()