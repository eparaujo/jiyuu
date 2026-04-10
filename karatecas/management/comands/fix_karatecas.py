from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string

from karatecas.models import Karateca
from dojos.models import DojoMembership
from dojos.choices import DojoRole


class Command(BaseCommand):
    help = "Cria usuários para karatecas sem user e vincula ao dojo"

    def handle(self, *args, **kwargs):

        created_users = 0
        linked_users = 0
        memberships_created = 0

        karatecas = Karateca.objects.filter(user__isnull=True)

        for k in karatecas:

            if not k.email:
                self.stdout.write(self.style.WARNING(
                    f"[IGNORADO] Sem email: {k.name}"
                ))
                continue

            user = User.objects.filter(username=k.email).first()

            if not user:
                password = get_random_string(8)

                user = User.objects.create_user(
                    username=k.email,
                    email=k.email,
                    password=password,
                    first_name=k.name
                )

                created_users += 1
                self.stdout.write(self.style.SUCCESS(
                    f"[USER CRIADO] {k.email} | senha: {password}"
                ))

            else:
                linked_users += 1
                self.stdout.write(
                    f"[USER EXISTENTE] {k.email}"
                )

            k.user = user
            k.save(update_fields=['user'])

            membership, created = DojoMembership.objects.get_or_create(
                user=user,
                dojo=k.dojo,
                defaults={"role": DojoRole.STUDENT}
            )

            if created:
                memberships_created += 1
                self.stdout.write(self.style.SUCCESS(
                    f"[MEMBERSHIP] {k.email} -> {k.dojo.name}"
                ))

        self.stdout.write("\n===== RESUMO =====")
        self.stdout.write(f"Users criados: {created_users}")
        self.stdout.write(f"Users vinculados: {linked_users}")
        self.stdout.write(f"Memberships criados: {memberships_created}")