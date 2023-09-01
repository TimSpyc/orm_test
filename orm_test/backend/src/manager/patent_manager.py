from django.db import models
from backend.models import GroupTable, DataTable, DataExtensionTable
from backend.src.auxiliary.manager import GeneralManager


class PatentGroup(GroupTable):
    """
    A Django model representing a part sold group.
    """
    patent_number = models.CharField(max_length=255, unique=True)

    @property
    def manager(self):
        return PatentManager

    def __str__(self):
        return f"PatentGroup {self.id}"


class Patent(DataTable):
    patent_group_id = models.ForeignKey(PatentGroup, on_delete= models.DO_NOTHING)
    remark = models.TextField(null=True)
    abstract = models.TextField(null=True)
    priority_date = models.DateTimeField(null=True)

    @property
    def group_object(self):
        return self.part_sold_group


class PatentClaim(DataExtensionTable):
    patent_id = models.ForeignKey(Patent, on_delete= models.DO_NOTHING)
    text = models.TextField(null=True)
    claim_number = models.IntegerField()

    @property
    def data_object(self):
        return self.part_sold



class PatentManager(GeneralManager):
    """
    A manager class for handling Patent-related operations, extending the GeneralManager.
    """
    group_model = PatentGroup
    data_model = Patent
    data_extension_model_list = [
        PatentClaim
    ]