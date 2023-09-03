# Responsible Maximilian Kelm
if __name__ == '__main__':
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'orm_test.settings')

    import django
    django.setup()

from example_db.populate import GeneralPopulate
from backend.models import AssetItemSiteConnectionGroup, AssetItemSiteConnection, AssetItemGroup, AssetSiteGroup

# TODO: Is there a possibility to depict the release of an asset item site connection?

def createAssetItemSiteConnectionGroupDict(cls):
    return {
        "asset_item_group": cls.getRandomForeignKeyRelation(AssetItemGroup),
        "asset_site_group": cls.getRandomForeignKeyRelation(AssetSiteGroup),
    }

def createAssetItemSiteConnectionDataDict(cls):
    return {}

class PopulateAssetItemSiteConnection(GeneralPopulate):
    group_definition = (
        AssetItemSiteConnectionGroup, 
        createAssetItemSiteConnectionGroupDict
    )
    data_definition = (
        AssetItemSiteConnection, 
        createAssetItemSiteConnectionDataDict
    )

    max_history_points = 1