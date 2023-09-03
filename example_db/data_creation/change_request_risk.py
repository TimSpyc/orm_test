# Responsible Maximilian Kelm
if __name__ == '__main__':
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'orm_test.settings')

    import django
    django.setup()

from example_db.populate import GeneralPopulate
from backend.models import ChangeRequestRiskGroup, ChangeRequestRisk

def createChangeRequestRiskGroupDict(cls):
    return {}

def createChangeRequestRiskDataDict(cls):
    return {}

class PopulateChangeRequestRisk(GeneralPopulate):
    group_definition = (ChangeRequestRiskGroup, createChangeRequestRiskGroupDict)
    data_definition = (ChangeRequestRisk, createChangeRequestRiskDataDict)

    max_history_points = 5