from django.db import models
from .abstract_models import ReferenceTable

class User(ReferenceTable):
    """
    A Django model representing a User with a Microsoft ID, name, last name,
    email, and last login date.
    """
    microsoft_id = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    last_login = models.DateTimeField(null=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Currency(ReferenceTable):
    """
    A Django model representing a Currency with a name, symbol, and exchange rate.
    """
    name = models.CharField(max_length=255)
    symbol = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.name}'