from django.apps import AppConfig


class KetquahoctapConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ketquahoctap'
    def ready(self):
        import ketquahoctap.signals
