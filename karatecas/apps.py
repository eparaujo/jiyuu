from django.apps import AppConfig


class KaratecasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'karatecas'

    def ready(self):
        import karatecas.signals
