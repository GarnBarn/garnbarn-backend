from django.apps import AppConfig


class GarnbarnApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'garnbarn_api'

    def ready(self):
        from garnbarn_api.services.scheduler import scheduler
        scheduler.start()
        from garnbarn_api.signals.on_save_assignment_signal import on_save_assignment
        from garnbarn_api.services.notification.send_notification import send_notification
