# Responsible Elias Bauer
from django.db import models
from backend.models import GroupTable, DataTable, DataExtensionTable
from backend.src.auxiliary.manager import GeneralManager

class CustomerVolumeGroup(GroupTable):
    """
    A Django model representing a customer volume group, which
    associates a customer volume group
    with a derivative constellium group.
    """
    derivative_constellium_group = models.ForeignKey(
        'DerivativeConstelliumGroup',
        on_delete=models.DO_NOTHING
    )

    @property
    def manager(self):
        return CustomerVolumeManager

    def __str__(self):
        return f'customer_volume_group with id {self.id}'

class CustomerVolume(DataTable):
    """
    A Django model representing a customer volume,
    including its project_phase_type, sop, eop,
    estimated price, estimated weight,
    description and used volume flag to mark the currently used customer volume.
    """
    customer_volume_group = models.ForeignKey(
        CustomerVolumeGroup, 
        on_delete=models.DO_NOTHING
    )
    project_phase_type = models.ForeignKey(
        'ProjectPhaseType',
        on_delete=models.DO_NOTHING
    )
    sop = models.DateField()
    eop = models.DateField()
    description = models.CharField(max_length=255)
    used_volume = models.BooleanField(default=False)

    @property
    def group_object(self):
        return self.customer_volume_group

    def __str__(self):
        return f'CustomerVolume with id {self.id}'

class CustomerVolumeVolume(DataExtensionTable):
    """
    ! Write your docstring here !
    """
    customer_volume = models.ForeignKey(CustomerVolume, on_delete=models.DO_NOTHING)
    volume = models.PositiveIntegerField()
    volume_date = models.DateField()

    @property
    def data_object(self):
        return self.customer_volume

    def __str__(self):
        return f"""
            Customer Volume Volume {self.id} for
            Customer Volume {self.customer_volume.id}
        """
    
class CustomerVolumeManager(GeneralManager):
    """
    ! Write your docstring here !
    """
    group_model = CustomerVolumeGroup
    data_model = CustomerVolume
    data_extension_model_list = [CustomerVolumeVolume]
    
    @property
    def current_volume(self) -> list[dict]:
        volume_list_of_dict = self.customer_volume_volume_list_of_dict
        return {volume_list_of_dict["volume_date"]: volume_list_of_dict["volume"]}
