from django.core.management import call_command

def truncate_all_tables():
    call_command('flush', '--noinput', reset_sequences=True, verbosity=0)