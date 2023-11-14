from django.core.management import call_command
from backend.models import DatabaseCache
from django.core.cache import cache

def truncate_all_tables():
    call_command('flush', '--noinput', reset_sequences=True, verbosity=0)

def clear_cache():
    DatabaseCache.objects.all().delete()
    cache.clear()  
    
def truncate_table(model):
    model.objects.all().delete()