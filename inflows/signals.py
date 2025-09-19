from django.db.models.signals import post_save
from django.dispatch import receiver # fica escutando e quando ocorrer um post_save, ele executa
from revenues.models import Revenue
from inflows.models import Inflow
from revenues.models import Revenue


@receiver(post_save, sender=Inflow) #aqui estamos falando que sempre que houver um post_save em Revenue, esta função será executada
def update_value(sender, instance, created, **kwargs):
    if created:
        if instance.value> 0:
            revenue = instance.revenue
            revenue.value += instance.value
        revenue.save() 