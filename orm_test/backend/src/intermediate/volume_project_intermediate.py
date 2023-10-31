# Responsible Elias Bauer

from backend.models import DerivativeConstelliumGroup
from backend.src.intermediate import (
    VolumeLmcDerivativeConstelliumIntermediate,
    VolumeCustomerDerivativeConstelliumIntermediate,
    intermediate_auxiliary
)
from backend.src.auxiliary.intermediate import GeneralIntermediate
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
        
        self.derivative_constellium_group_dict_list = \
            list(DerivativeConstelliumGroup.objects.filter(
                project_group_id=project_group_id
            ).values())
        
        self.search_date = search_date

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
            
            total_volume = self.__updateTotalVolume(total_volume, inter_obj)


        return total_volume, total_volume_derivative

    def __updateTotalVolume(
        self,
        total_volume: list,
        inter_obj: GeneralIntermediate
    ) -> list:
        '''
        Description:
        ------------
        Updates the total volume by adding the volume data from
        the intermediate object to the existing total volume.

        Inputs/Parameters:
        ------------------
        total_volume : list
            A list of dictionaries containing the total volume data.
        inter_obj : GeneralIntermediate
            An object containing the intermediate volume data.

        Returns:
        --------
        total_volume : list
            A list of dictionaries containing the updated total volume data.
        '''
        for volume_data in inter_obj.volume:
            datum = volume_data['volume_date']
            volume = volume_data['volume']

            existing_volume = next(
                (x for x in total_volume if x['volume_date'] == datum),
                None
            )
            if existing_volume is None:
                total_volume.append({
                    'volume_date': datum,
                    'volume': volume,
                })
            else:
                existing_volume['volume'] += volume
        return total_volume