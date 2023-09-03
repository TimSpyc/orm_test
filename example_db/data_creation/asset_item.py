# Responsible Maximilian Kelm
if __name__ == '__main__':
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'orm_test.settings')

    import django
    django.setup()

from example_db.populate import GeneralPopulate
from backend.models import AssetItemGroup, AssetItem

def createAssetItemGroupDict(cls):
    return {}

def createAssetItemDataDict(cls):
    return {
        "name": cls.getRandomText(),
        "max_width": cls.getRandomInteger(1, 3),
        "max_height": cls.getRandomInteger(1, 3),
        "description": cls.getRandomDescription(),
    }

class PopulateAssetItem(GeneralPopulate):
    group_definition = (AssetItemGroup, createAssetItemGroupDict)
    data_definition = (AssetItem, createAssetItemDataDict)

    max_history_points = 5