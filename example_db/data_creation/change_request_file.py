# Responsible Maximilian Kelm
if __name__ == '__main__':
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'orm_test.settings')

    import django
    django.setup()

from example_db.populate import GeneralPopulate
from backend.models import ChangeRequestFileGroup, ChangeRequestFile

def createChangeRequestFileGroupDict(cls):
    return {}

def createChangeRequestFileDataDict(cls):
    return {}

class PopulateChangeRequestFile(GeneralPopulate):
    group_definition = (ChangeRequestFileGroup, createChangeRequestFileGroupDict)
    data_definition = (ChangeRequestFile, createChangeRequestFileDataDict)

    max_history_points = 5