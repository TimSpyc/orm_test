# Responsible Elias Bauer

from backend.models import DerivativeConstelliumGroup
from backend.src.intermediate import (
    VolumeLmcDerivativeConstelliumIntermediate,
    VolumeCustomerDerivativeConstelliumIntermediate,
    intermediate_auxiliary
)
from backend.src.auxiliary.intermediate import GeneralIntermediate
import backend.src.auxiliary.list_of_dicts  as inter_lod
from datetime import datetime


class VolumeProjectIntermediate(GeneralIntermediate):
    relevant_scenario_keys = []
    
    def __init__(
        self,
        project_group_id: int,
        VolumeDerivativeIntermediateClass: GeneralIntermediate,
        search_date: datetime | None = None,
        scenario_dict: dict = {},
    ):

        self.VolumeDerivativeIntermediateClass = VolumeDerivativeIntermediateClass
        intermediate_auxiliary.checkValidityOfVolumeDerivativeIntermediateClass(
            attribute_name = self.VolumeDerivativeIntermediateClass,
            valid_classes = [
                VolumeLmcDerivativeConstelliumIntermediate,
                VolumeCustomerDerivativeConstelliumIntermediate
            ]
        )
        self.search_date = search_date
        self.derivative_constellium_group_dict_list = \
            list(DerivativeConstelliumGroup.objects.filter(
                project_group_id=project_group_id
            ).values())

        self.volume, self.volume_derivative = self.getVolume()

        super().__init__(
            search_date,
            scenario_dict,
        )

    def getVolume(self) -> list:
        """
        Description:
        --------
        Get the total volume of all derivative constellium groups
        based on the derivative_constellium_group_dict_list.

        Returns:
        --------
        total_volume : list of dictionaries
            The total volume of all derivative constellium groups.
        """
        total_volume = []
        total_volume_derivative = []

        for data in self.derivative_constellium_group_dict_list:
            derivative_constellium_group_id = data['id']
            inter_obj = self.VolumeDerivativeIntermediateClass(
                derivative_constellium_group_id=derivative_constellium_group_id,
                search_date=self.search_date,
            )

            total_volume_derivative.append({
                'derivative_constellium_group_id': derivative_constellium_group_id,
                'volume_derivative': inter_obj.volume
                })

            total_volume += inter_obj.volume
        
        return inter_lod.groupListOfDictsByListOfStrings(
            result_list_dict=total_volume,
            group_by_key_list=['date']
        )
