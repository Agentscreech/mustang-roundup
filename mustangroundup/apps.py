from django.apps import AppConfig


class MustangroundupConfig(AppConfig):
    name = 'mustangroundup'

    def ready(self):
        from . import signals
