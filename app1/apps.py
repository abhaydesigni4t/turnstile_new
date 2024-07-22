from django.apps import AppConfig
from django.db.models.signals import post_migrate, post_save, post_delete

class App1Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app1'

    def ready(self):
        import app1.signals
    
