if __name__ == '__main__':
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'orm_test.settings')

    import django
    django.setup()

from example_db.populate import GeneralPopulate
from backend.models import PartRecipient, PartRecipientGroup

def createPartRecipientGroupDict(cls):
    return {"number": f'{cls.getRandomInteger(1, 1000000):07}'}

def createPartRecipientDataDict(cls):
    return {"description": cls.getRandomDescription()}

class PopulatePartRecipient(GeneralPopulate):
    group_definition = (PartRecipientGroup, createPartRecipientGroupDict)
    data_definition = (PartRecipient, createPartRecipientDataDict)

    max_history_points = 1
