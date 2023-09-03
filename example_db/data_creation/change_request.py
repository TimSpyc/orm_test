# Responsible Maximilian Kelm
if __name__ == '__main__':
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'orm_test.settings')

    import django
    django.setup()

from example_db.populate import GeneralPopulate
from backend.models import ChangeRequestGroup, ChangeRequest, ProjectGroup, DerivativeConstelliumGroup

def createChangeRequestGroupDict(cls):
    return {
        "project_group": cls.getRandomForeignKeyRelation(ProjectGroup),
        # TODO: Change to automatically ascending number!
        "change_request_number": cls.getRandomInteger(1, 5),
    }

def createChangeRequestDataDict(cls):
    return {
        "derivative_constellium_group": 
            cls.getRandomForeignKeyRelation(DerivativeConstelliumGroup),
        # TODO: Create general functions to get realistic data! (part, ecr)
        "customer_part_number": cls.getRandomText(15),
        "customer_part_name": cls.getRandomText(15),
        "ECR_number": cls.getRandomText(10),
        # TODO: Create general functions to get realistic data! (approval state)
        # "customer_approval": random.choice([True, False, None]),
        # "internal_approval": random.choice([True, False, None]),
        # TODO: Create data for part and file!
        # "before_change_part": cls.getRandomForeignKeyRelation(Part),
        # "before_change_image": cls.getRandomForeignKeyRelation(File),
        # "after_change_part": cls.getRandomForeignKeyRelation(Part),
        # "after_change_image": cls.getRandomForeignKeyRelation(File),
        "description": cls.getRandomDescription(),
    }

class PopulateChangeRequest(GeneralPopulate):
    group_definition = (ChangeRequestGroup, createChangeRequestGroupDict)
    data_definition = (ChangeRequest, createChangeRequestDataDict)

    max_history_points = 5