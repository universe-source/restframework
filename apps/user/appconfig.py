from django.apps import AppConfig


class UserAppConfig(AppConfig):
    name = 'apps.user'
    verbose_name = 'application user'

    def ready(self):
        print('UserAppConfig Ready ...')
        import apps.user.signals
