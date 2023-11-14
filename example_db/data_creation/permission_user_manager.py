# Responsible Maximilian Kelm
if __name__ == '__main__':
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'orm_test.settings')

    import django
    django.setup()

from example_db.populate import GeneralPopulate
from backend.models import PermissionUserGroup, PermissionUser, AssetItemSiteConnectionGroup, User, PermissionType

# TODO: Implement the possibility to fake a confirmation process (decorator?)
# -> Therefore the user and creator must be the same for the first data point.
# Also the is_accepted must be Null.
# -> The second data point must have the manager as creator and True or False
# as is_accepted value.

def createPermissionUserGroupDict(cls):
    return {
        "asset_item_site_connection_group": cls.getRandomForeignKeyRelation(
            AssetItemSiteConnectionGroup
        ),
        "user": cls.getRandomForeignKeyRelation(User)
    }

def createPermissionUserDataDict(cls):
    return {
        "permission_type": cls.getRandomForeignKeyRelation(PermissionType),
        "is_accepted": cls.getRandomBoolean(can_be_none=True)
    }

class PopulatePermissionUser(GeneralPopulate):
    group_definition = (PermissionUserGroup, createPermissionUserGroupDict)
    data_definition = (PermissionUser, createPermissionUserDataDict)