from django.core.management.base import BaseCommand
from backend.src.auxiliary.manager import transferToSnakeCase
import os

class Command(BaseCommand):
    help = """
        Create a manager.py in the right directory and 
        fill it with the basic structure.
    """

    def add_arguments(self, parser):
        parser.add_argument(
            'manager_name', 
            type=str, 
            help='The name of the Manager to create'
        )

    def handle(self, *args, **options):
        manager_name = options['manager_name']
        manager_name_snake_case = transferToSnakeCase(manager_name)
        file_path = os.path.join(
            os.getcwd(), 
            f'backend/src/manager/{manager_name_snake_case}_manager.py'
        )
        
        with open(file_path, 'w') as f:
            f.write(f'''# Responsible ?
from django.db import models
from backend.models import GroupTable, DataTable#, DataExtensionTable
from backend.src.auxiliary.manager import GeneralManager

# TODO's -----------------------------------------------------------------------
# - General:
# - [ ] Add responsible person
# - [ ] Add custom imports (optional)
# 
# - GroupTable:
# - [ ] Define custom group fields
# - [ ] Import GroupTable into models __init__.py
# - [ ] Write docstring for GroupTable
# 
# - DataTable:
# - [ ] Define custom data fields
# - [ ] Import DataTable into models __init__.py
# - [ ] Write docstring for DataTable
# 
# - DataExtensionTables (optional):
# - [ ] Name the data extension fields
# - [ ] Define custom data extension fields
# - [ ] Import DataExtensionTable into models __init__.py
# 
# - Manager:
# - [ ] Append data extension tables to the list (optional)
# - [ ] Import Manager into manager __init__.py
# - [ ] Write docstring for Manager
# ------------------------------------------------------------------------------

class {manager_name}Group(GroupTable):
    """
    ! Write your docstring here !
    """
    # TODO: Define custom data fields here!

    @property
    def manager(self):
        return {manager_name}Manager

    def __str__(self):
        return f'{manager_name} Group with id {{self.id}}'

class {manager_name}(DataTable):
    """
    ! Write your docstring here !
    """
    {manager_name_snake_case}_group = models.ForeignKey(
        {manager_name}Group, 
        on_delete=models.DO_NOTHING
    )
    # TODO: Define custom data fields here!

    @property
    def group_object(self):
        return self.{manager_name_snake_case}_group

    def __str__(self):
        return f'{manager_name} with id {{self.id}}'
    
# class ExampleName(DataExtensionTable):
#     """
#     ! Write your docstring here !
#     """
#     {manager_name_snake_case} = models.ForeignKey(
#         {manager_name}, 
#         on_delete=models.DO_NOTHING
#     )
#     # TODO: Define custom data fields here!
# 
#     @property
#     def data_object(self):
#         return self.{manager_name}

class {manager_name}Manager(GeneralManager):
    """
    ! Write your docstring here !
    """
    group_model = {manager_name}Group
    data_model = {manager_name}
    data_extension_model_list = []''')

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created manager "{manager_name}"'
            )
        )