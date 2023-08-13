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
    abbreviation = models.CharField(max_length=3)
    symbol = models.CharField(max_length=2)

    def __str__(self):
        return f'{self.name}'
    
class NormType(ReferenceTable):
    """
    A Django model representing a NormType with a name.
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.name}'

class PartType(ReferenceTable):
    """
    A Django model representing a PartType with a name.
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.name}'

class PartPosition(ReferenceTable):
    """
    A Django model representing a PartPosition with a name.
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.name}'

class SemiFinishedProductType(ReferenceTable):
    """
    A Django model representing a SemiFinishedProductType with a name.
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.name}'
    
class MaterialType(ReferenceTable):
    """
    A Django model representing a MaterialType with a name.
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.name}'
    
class PartSoldPriceComponentType(ReferenceTable):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.name}'

class PriceUploadSource(ReferenceTable):
    name = models.CharField(max_length=255) 

    def __str__(self):
        return f'{self.name}'

class SavingUnit(ReferenceTable):
    name = models.CharField(max_length=255) 

    def __str__(self):
        return f'{self.name}'

class PartSoldMaterialType(ReferenceTable):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.name}'

class PartSoldMaterialPriceType(ReferenceTable):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.name}'

class MaterialType(ReferenceTable):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.name}'


class DerivativeType(ReferenceTable):
    """
    A Django model representing a derivative type, which includes a name.
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class PredictionAccuracy(ReferenceTable):
    """
    A Django model representing a prediction accuracy, which includes a name.
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class ProjectUserRole(ReferenceTable):
    """
    A Django model representing a project user role, which includes a role
    name.
    """
    role_name = models.CharField(max_length=255)

    def __str__(self):
        return self.role_name


class RevisionLMC(ReferenceTable):
    revision_date = models.DateField()

    def __str__(self):
        return self.revision_date.strftime('%Y-%m')
    
    class Meta:
        get_latest_by = "revision_date"

class ProjectStaffCostTask(ReferenceTable):
    name = models.CharField(max_length=30)
    description = models.TextField()

    def __str__(self):
        return self.name