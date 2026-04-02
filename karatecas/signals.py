from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string

from karatecas.models import Karateca
from dojos.models import DojoMembership, Dojo
from dojos.choices import DojoRole


@receiver(post_save, sender=Karateca)
def ensure_user_and_membership(sender, instance, created, **kwargs):

    # 🔒 Se já tem user, não faz nada (evita loop)
    if instance.user:
        user = instance.user
    else:
        if not instance.email:
            return

        user = User.objects.filter(username=instance.email).first()

        if not user:
            password = get_random_string(8)

            user = User.objects.create_user(
                username=instance.email,
                email=instance.email,
                password=password,
                first_name=instance.name
            )

        # 🔹 vincula user ao karateca
        instance.user = user
        instance.save(update_fields=['user'])

    # 🔴 GARANTE MEMBERSHIP NO DOJO DO KARATECA
    if instance.dojo:
        DojoMembership.objects.get_or_create(
            user=user,
            dojo=instance.dojo,
            defaults={"role": DojoRole.STUDENT}
        )

    # 🔴 REGRA NOVA: PERFIS GLOBAIS EM TODOS OS DOJOS
    global_roles = [
        DojoRole.OWNER,
        DojoRole.SENSEI,
        DojoRole.ADMIN,
        DojoRole.EXAMINER,
    ]

    user_roles = DojoMembership.objects.filter(user=user).values_list('role', flat=True)

    if any(role in global_roles for role in user_roles):
        dojos = Dojo.objects.all()

        for dojo in dojos:
            DojoMembership.objects.get_or_create(
                user=user,
                dojo=dojo,
                defaults={"role": user_roles[0]}  # mantém um dos roles já existentes
            )