from django.db.models.signals import post_save
from django.dispatch import receiver # fica escutando e quando ocorrer um post_save, ele executa
from revenues.models import Revenue
from karatecas.models import Karateca


#@receiver(post_save, sender=Karateca) #aqui estamos falando que sempre que houver um post_save em Revenue, esta função será executada
#def increment_total_karatecas(sender, instance, created, **kwargs):
#    if created:
#        if instance.total_karatecas > 0:
#            karatecas = instance.total_karatecas
#            karatecas.total_karatecas += instance.total_karatecas
#            karatecas.save()