from django.core.management.base import BaseCommand
from django.core.management.commands import makemigrations
from backend.src.auxiliary.string_modification import knowledgeHubLogoPrint
from backend.src.auxiliary.db import truncate_all_tables
from backend.models.populate import PopulateManager
from backend.src import manager

class Command(BaseCommand):
    help = """
        Create a manager.py in the right directory and 
        fill it with the basic structure.
    """
    requires_migrations_checks = True

    def add_arguments(self, parser):
        parser.add_argument(
            "--debug",
            action="store_true",
            help="Only populate one object for every manager",
        )

    def handle(self, *args, **options):
        self.debug = options['debug']
        knowledgeHubLogoPrint()
        self.stdout.write(
            "This script will truncate all tables before filling it!",
            ending="\n"
        )
        
        command = input("Do you want to proceed? (y/N): ")
        if command not in ['y', 'Y', 'yes', 'Yes']:
            print('aborting...')
            return
        
        truncate_all_tables()

        for manager_name in dir(manager):
            manager_class = getattr(manager, manager_name)
            
            if not isinstance(manager_class, type):
                continue

            if manager_class.__name__ in [
                "BillOfMaterialManager",
                "CrossSectionManager"
            ]:
                continue

            is_external_data_manager = False
            for parent_class in manager_class.__bases__:
                if parent_class.__name__ == "ExternalDataManager":
                    is_external_data_manager = True
            
            if is_external_data_manager:
                continue

            self.stdout.write(
                f"Populate: {manager_class.__name__}",
                ending="\n"
            )

            if self.debug:
                PopulateManager(manager_class).populate()
            else:
                PopulateManager(manager_class).populateMany()

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully filled db!'
            )
        )