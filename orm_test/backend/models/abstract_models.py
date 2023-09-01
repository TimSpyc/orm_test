from django.db import models
from django.utils import timezone
from datetime import datetime

if __name__ == '__main__':
    from backend.src.auxiliary.manager import GeneralManager

class GroupTable(models.Model):
    """
    An abstract Django model for representing group tables. These tables
    are used to group data, so its possible to have a history of the data in
    the connected Data Tables.
    Each Group Table needs to have a manager @property that returns a
    GeneralManager class.
    Use this table with the GeneralManager.
    """
    table_type = 'GroupTable'

    def getManager(
        self, 
        search_date: datetime, 
    ) -> 'GeneralManager':
        return self.manager(self.id, search_date)

    class Meta:
        abstract = True

class ReferenceTable(models.Model):
    """
    An abstract Django model for representing reference tables. These tables
    are meant to be used for reference data aka. data that is not expected to
    change. This must not ne used for user changeable data.
    """
    active = models.BooleanField(default=True)
    table_type = 'ReferenceTable'
    class Meta:
        abstract = True

class DataTable(models.Model):
    """
    An abstract Django model for representing data tables. These tables
    are meant to be used for data that is expected to change. With the connected
    Group Table it is possible to have a history of the data.
    Each creation of a new data entry must be connected to a user and the date
    of creation. The active field is used to mark data entries as deleted.
    Each Data Table needs to have a group_object @property that returns the
    connected Group Table object.
    Use this table with the GeneralManager.
    """
    date = models.DateTimeField()
    creator = models.ForeignKey("User", on_delete=models.DO_NOTHING)
    active = models.BooleanField(default=True)
    table_type = 'DataTable'
    class Meta:
        abstract = True


class DataExtensionTable(models.Model):
    """
    An abstract Django model for representing data extension tables. These tables
    are meant to be used for data that is expected to change on the same date as
    the connected Data Table. With the connected Group Table it is possible to
    have a history of the data. This table type is used if you have a 1:n
    relation to the Data Table.
    Each Data Extension Table needs to have a data_object @property that returns
    the connected Data Table object.
    Use this table with the GeneralManager.
    """
    table_type = 'DataExtensionTable'
    class Meta:
        abstract = True


class ExternalDataTable(models.Model):
    """
    An abstract Django model for representing external data tables. These tables
    are meant to be used for data that is not handlebar by the Group, Data and
    Data Extension Tables. Use this table with the ExternalDataManager.
    """
    date = models.DateTimeField(default=timezone.now)
    table_type = 'ExternalDataTable'
    class Meta:
        abstract = True