from django.core.management import call_command
from backend.models import CacheManager, CacheIntermediate
from django.core.cache import cache

def truncate_all_tables():
    call_command('flush', '--noinput', reset_sequences=True, verbosity=0)

def clear_cache():
    CacheManager.objects.all().delete()
    CacheIntermediate.objects.all().delete()
    cache.clear()