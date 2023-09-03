# Responsible Maximilian Kelm
if __name__ == '__main__':
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'orm_test.settings')

    import django
    django.setup()

from example_db.populate import GeneralPopulate
from backend.models import AssetLayoutGroup, AssetLayout, User

def createAssetLayoutGroupDict(cls):
    return {
        "user": cls.getRandomForeignKeyRelation(User),
        "grid_size": cls.getRandomInteger(1, 3)
    }

def createAssetLayoutDataDict(cls):
    return {
        "name": cls.getRandomText(),
        "height": cls.getRandomInteger(1, 3),
        "width": cls.getRandomInteger(1, 3),
        # TODO: Should the coordinates be realistic? YES!
        "x_coordinate": cls.getRandomInteger(1, 3),
        "y_coordinate": cls.getRandomInteger(1, 3),
        "description": cls.getRandomDescription(),
    }

class PopulateAssetLayout(GeneralPopulate):
    group_definition = (AssetLayoutGroup, createAssetLayoutGroupDict)
    data_definition = (AssetLayout, createAssetLayoutDataDict)

    max_history_points = 5