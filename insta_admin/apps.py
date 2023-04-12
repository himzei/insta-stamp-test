from django.apps import AppConfig


class InstaAdminConfig(AppConfig):
    name = 'insta_admin'

    def ready(self): 
        from jobs import updater
        updater.start()
