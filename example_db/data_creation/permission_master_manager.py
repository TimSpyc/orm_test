# Responsible Maximilian Kelm
if __name__ == '__main__':
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'orm_test.settings')

    import django
    django.setup()

from example_db.populate import GeneralPopulate
from backend.models import PermissionMasterGroup, PermissionMaster, AssetItemSiteConnectionGroup, User

def createPermissionMasterGroupDict(cls):
    return {
        "asset_item_site_connection_group": cls.getRandomForeignKeyRelation(
            AssetItemSiteConnectionGroup
        ),
        "user": cls.getRandomForeignKeyRelation(User)
    }

def createPermissionMasterDataDict(cls):
    return {}

class PopulatePermissionMaster(GeneralPopulate):
    group_definition = (PermissionMasterGroup, createPermissionMasterGroupDict)
    data_definition = (PermissionMaster, createPermissionMasterDataDict)

    max_history_points = 1