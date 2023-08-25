# Responsible Maximilian Kelm
from django.db import models
from backend.models import GroupTable, DataTable
from backend.src.auxiliary.manager import GeneralManager

class ChangeRequestGroup(GroupTable):
    """
    A Django model representing a change request group.
    """
    project_group = models.ForeignKey(
        'ProjectGroup', 
        on_delete=models.DO_NOTHING, 
    )
    change_request_number = models.PositiveSmallIntegerField(null=False)

    @property
    def manager(self):
        return ChangeRequestManager
    
    class Meta:
        unique_together = (
            'project_group', 'change_request_number'
        )

    def __str__(self):
        return f'ChangeRequest Group with id {self.id}'
    
    def save(self, *args, **kwargs):
        if self.change_request_number is None:
            change_request_group_list = self.objects.all().filter(
                project_group_id=self.project_group.id
            )

            if len(change_request_group_list) == 0:
                self.change_request_number = 1
            else:
                self.change_request_number =\
                    change_request_group_list.objects.latest(
                        'change_request_number'
                    ).change_request_number + 1

        super(ChangeRequestGroup, self).save(*args, **kwargs)

class ChangeRequest(DataTable):
    """
    A Django model representing a change request.
    """
    change_request_group = models.ForeignKey(
        ChangeRequestGroup, 
        on_delete=models.DO_NOTHING,
    )
    derivative_constellium_group = models.ForeignKey(
        'DerivativeConstelliumGroup', 
        on_delete=models.DO_NOTHING,
    )
    # TODO: Add volume_customer_group_id
    customer_part_number = models.CharField(max_length=255, null=True)
    customer_part_name = models.CharField(max_length=255, null=True)
    ECR_number = models.CharField(max_length=255, null=True)
    customer_approval = models.BooleanField(null=True)
    internal_approval = models.BooleanField(null=True)
    before_change_part = models.ForeignKey(
        'PartGroup', 
        on_delete=models.DO_NOTHING,
        related_name='before_change_part',
    )
    before_change_image = models.ForeignKey(
        'FileGroup', 
        on_delete=models.DO_NOTHING,
        related_name='before_change_image',
    )
    after_change_part = models.ForeignKey(
        'PartGroup', 
        on_delete=models.DO_NOTHING,
        related_name='after_change_part',
    )
    after_change_image = models.ForeignKey(
        'FileGroup', 
        on_delete=models.DO_NOTHING,
        related_name='after_change_image',
    )
    description = models.TextField(null=True)

    @property
    def group(self):
        return self.change_request_group

    def __str__(self):
        return f'ChangeRequest with id {self.id}'

class ChangeRequestManager(GeneralManager):
    """
    A manager class for handling change request related operations, extending 
    the GeneralManager.

    Attributes:
        group_model (models.Model): The ChangeRequestGroup model.
        data_model (models.Model): The ChangeRequest model.
    """
    group_model = ChangeRequestGroup
    data_model = ChangeRequest
    data_extension_model_list = []

    def __init__(
        self, change_request_group_id, search_date=None, use_cache=True
    ):
        """
        Initialize a ChangeRequestManager instance.

        Args:
            change_request_group_id (int): 
                The ID of the ChangeRequestGroup instance.
            search_date (datetime.datetime, optional): 
                The date used for filtering data. Defaults to None.
            use_cache (bool, optional): 
                Whether to use the cache for data retrieval. Defaults to True.
        """
        super().__init__(
            group_id=change_request_group_id, 
            search_date=search_date, 
            use_cache=use_cache
        )