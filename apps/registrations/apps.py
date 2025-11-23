from django.apps import AppConfig


class RegistrationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.registrations'
    verbose_name = 'Cadastros'

    def ready(self):
        import apps.registrations.signals.subscription