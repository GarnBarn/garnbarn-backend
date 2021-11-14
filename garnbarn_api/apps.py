from django.apps import AppConfig

from garnbarn_api import scheduler


class GarnbarnApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'garnbarn_api'

    def ready(self):
        scheduler.start()
