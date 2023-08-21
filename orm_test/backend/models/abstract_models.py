from django.db import models
from datetime import datetime
# from .reference_models import User

class GroupTable(models.Model):
    """
    An abstract Django model for representing group tables.
    """
    table_type = 'GroupTable'
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
    date = models.DateTimeField(default=datetime.now())
    table_type = 'ExternalDataTable'
    class Meta:
        abstract = True