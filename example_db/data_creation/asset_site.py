# Responsible Maximilian Kelm
if __name__ == '__main__':
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'orm_test.settings')

    import django
    django.setup()

from example_db.populate import GeneralPopulate
from backend.models import AssetSiteGroup, AssetSite

def createAssetSiteGroupDict(cls):
    return {}

def createAssetSiteDataDict(cls):
    return {
        "name": cls.getRandomText(25),
    }

class PopulateAssetSite(GeneralPopulate):
    group_definition = (AssetSiteGroup, createAssetSiteGroupDict)
    data_definition = (AssetSite, createAssetSiteDataDict)

    max_history_points = 5