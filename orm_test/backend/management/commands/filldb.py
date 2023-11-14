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
            help="Only populate a small number of objects for every manager",
        )
        parser.add_argument(
            "--truncate",
            action="store_true",
            help="Truncate tables and update references",
        )
        parser.add_argument(
            "--update-references",
            action="store_true",
            help="Update references to newest version",
        )

    def handle(self, *args, **options):
        self.debug = options['debug']
        self.truncate = options['truncate']
        self.update_references = options['update_references']

        if self.truncate and not self.update_references:
            self.update_references = True

        # TODO: Handle reference tables! -> Update references?

        if self.truncate:
            self.stdout.write(
                f"Truncate all tables",
                ending="\n"
            )
            truncate_all_tables()

        for manager_name in dir(manager):
            manager_class = getattr(manager, manager_name)
            
            if not isinstance(manager_class, type):
                continue

            # NOTE: The populate function for bom is not defined correctly
            # to work with the manager!
            if manager_class.__name__ in ["BillOfMaterialManager"]:
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