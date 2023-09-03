# Responsible Maximilian Kelm
if __name__ == '__main__':
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'orm_test.settings')

    import django
    django.setup()

from example_db.populate import GeneralPopulate
from backend.models import ChangeRequestFeasibilityGroup, ChangeRequestFeasibility

def createChangeRequestFeasibilityGroupDict(cls):
    return {}

def createChangeRequestFeasibilityDataDict(cls):
    return {}

class PopulateChangeRequestFeasibility(GeneralPopulate):
    group_definition = (
        ChangeRequestFeasibilityGroup, 
        createChangeRequestFeasibilityGroupDict
    )
    data_definition = (
        ChangeRequestFeasibility, 
        createChangeRequestFeasibilityDataDict
    )

    max_history_points = 5