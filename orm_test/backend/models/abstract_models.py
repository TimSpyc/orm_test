from django.db import models
from django.utils import timezone
from datetime import datetime

if __name__ == '__main__':
    from backend.src.auxiliary.manager import GeneralManager

class GroupTable(models.Model):
    """
    An abstract Django model for representing group tables.
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
    An abstract Django model for representing reference tables.
    """
    active = models.BooleanField(default=True)
    table_type = 'ReferenceTable'
    class Meta:
        abstract = True

class DataTable(models.Model):
    """
    An abstract Django model for representing data tables, including date,
    creator, and active status.
    """
    date = models.DateTimeField()
    creator = models.ForeignKey("User", on_delete=models.DO_NOTHING)
    active = models.BooleanField(default=True)
    table_type = 'DataTable'
    class Meta:
        abstract = True


class DataExtensionTable(models.Model):
    """
    An abstract Django model for representing data extension tables.
    """
    table_type = 'DataExtensionTable'
    class Meta:
        abstract = True


class ExternalDataTable(models.Model):
    """
    An abstract Django model for representing external data tables.
    """
    date = models.DateTimeField(default=timezone.now)
    table_type = 'ExternalDataTable'
    class Meta:
        abstract = True