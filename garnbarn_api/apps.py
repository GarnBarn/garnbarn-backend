from django.apps import AppConfig


class GarnbarnApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'garnbarn_api'

    def ready(self):
        from garnbarn_api.scheduler import scheduler
