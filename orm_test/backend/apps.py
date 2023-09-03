from django.apps import AppConfig
from django.conf import settings

class BackendConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'backend'

    def ready(self):
        try:
            if settings.USE_CACHE:
                print('using cache')
                from backend.src.auxiliary.db import clear_cache
                clear_cache()
        except:
            print('cache currently not available')