from django.db import models
from backend.models import GroupTable, DataTable, DataExtensionTable
from backend.src.auxiliary.manager import GeneralManager


class PatentGroup(GroupTable):
    """
    A Django model representing a PatentGroup with a patent number.
    """

    patent_number = models.CharField(max_length=100, unique=True)

    class meta:
        unique_together = ('patent_number')

    @property
    def manager(self):
        return PatentManager

    def __str__(self):
        return f"PatentGroup {self.id}"

class Patent(DataTable):
    patent_group = models.ForeignKey(PatentGroup, on_delete= models.DO_NOTHING)
    remark = models.TextField(null=True)
    abstract = models.TextField(null=True)
    priority_date = models.DateTimeField(null=True)
    patent_tag = models.ManyToManyField('PatentTag', blank=True)
    status = models.ForeignKey('PatentStatus', on_delete=models.DO_NOTHING)
    inventor = models.ManyToManyField('User', related_name='inventor', blank=True)
    drawing = models.ManyToManyField('FileGroup', blank=True)
    part_group = models.ManyToManyField('PartGroup', blank=True)

    @property
    def group_object(self):
        return self.patent_group


class PatentClaim(DataExtensionTable):
    patent = models.ForeignKey(Patent, on_delete= models.DO_NOTHING)
    text = models.TextField()
    claim_number = models.IntegerField()

    @property
    def data_object(self):
        return self.patent
    
    class Meta:
        unique_together = ['patent', 'claim_number']


class PatentManager(GeneralManager):
    """
    A manager class for handling Patent-related operations, extending the 
    General Manager
    """
    group_model = PatentGroup
    data_model = Patent
    data_extension_model_list = [
        PatentClaim
    ]