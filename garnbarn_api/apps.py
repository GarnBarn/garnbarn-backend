from django.apps import AppConfig
from scheduler import updater


class GarnbarnApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'garnbarn_api'

    def ready(self):
        updater.start()
