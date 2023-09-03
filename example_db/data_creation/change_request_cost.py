# Responsible Maximilian Kelm
if __name__ == '__main__':
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'orm_test.settings')

    import django
    django.setup()

from example_db.populate import GeneralPopulate
from backend.models import ChangeRequestCostGroup, ChangeRequestCost

def createChangeRequestCostGroupDict(cls):
    return {}

def createChangeRequestCostDataDict(cls):
    return {}

class PopulateChangeRequestCost(GeneralPopulate):
    group_definition = (ChangeRequestCostGroup, createChangeRequestCostGroupDict)
    data_definition = (ChangeRequestCost, createChangeRequestCostDataDict)

    max_history_points = 5