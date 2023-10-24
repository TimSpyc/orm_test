if __name__ == '__main__':
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'orm_test.settings')

    import django
    django.setup()

from example_db.populate import GeneralPopulate
from backend.models import Project, ProjectGroup

def createProjectGroupDict(cls):
    return {}

def createProjectDataDict(cls):
    project_number = f'AP{cls.getRandomInteger(10000, 99999)}'
    if cls.randomChoice(0.8):
        project_number = f'CST-{cls.getRandomInteger(100, 999)}'

    return {
        "name": cls.getRandomText(),
        "project_number": project_number,
    }

class PopulateProject(GeneralPopulate):
    group_definition = (ProjectGroup, createProjectGroupDict)
    data_definition = (Project, createProjectDataDict)

    max_history_points = 9