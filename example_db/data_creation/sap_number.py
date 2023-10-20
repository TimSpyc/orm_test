if __name__ == '__main__':
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'orm_test.settings')

    import django
    django.setup()

from example_db.populate import GeneralPopulate
from backend.models import SapNumber, SapNumberGroup

def createSapNumberGroupDict(cls):
    return {"sap_number": f'{cls.getRandomInteger(6000000, 7000000):07}'}

def createSapNumberDataDict(cls):
    return {
        "alu_net_weight": cls.getRandomFloat(0.5, 75.5),
        "description": cls.getRandomDescription(),
    }

class PopulateSapNumber(GeneralPopulate):
    group_definition = (SapNumberGroup, createSapNumberGroupDict)
    data_definition = (SapNumber, createSapNumberDataDict)

    max_history_points = 1
