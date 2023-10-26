# Responsible Elias Bauer

from backend.models import DerivativeConstelliumGroup
from backend.src.intermediate import (
    VolumeLmcDerivativeConstelliumIntermediate,
    VolumeCustomerDerivativeConstelliumIntermediate
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

        self.__checkValidityOfVolumeDerivativeIntermediateClass(
            VolumeDerivativeIntermediateClass
        )
        
        self.VolumeDerivativeIntermediateClass = VolumeDerivativeIntermediateClass
        
        self.derivative_constellium_group_dict_list = \
            list(DerivativeConstelliumGroup.objects.filter(
                project_group_id=project_group_id
            ).values())
        
        self.search_date = search_date

        self.volume = self.getVolume()

        super().__init__(
            search_date,
            scenario_dict,
        )

    def __checkValidityOfVolumeDerivativeIntermediateClass(
        VolumeDerivativeIntermediateClass: GeneralIntermediate
    ):
        if VolumeDerivativeIntermediateClass not in [
            VolumeLmcDerivativeConstelliumIntermediate,
            VolumeCustomerDerivativeConstelliumIntermediate
        ]:
            raise ValueError(
                f"{VolumeDerivativeIntermediateClass} is not supported"
            )

    def getVolume(self) -> list:
        """
        Description:
        --------
        Get the total volume of all derivative constellium groups
        based on the derivative_constellium_group_dict_list.

        Declare:
        --------
        total_volume : list of dictionaries
            The total volume of all derivative constellium groups.
        data : dictionary
            The data of the derivative constellium group dictionary list.
        derivative_constellium_group_id : int
            The ID of the derivative constellium group.
        inter_obj : VolumeDerivativeIntermediateClass object
            The volume derivative intermediate class object.
        volume_data : dictionary
            The volume data of the volume derivative intermediate class object.
        datum : datetime object
            The date of the volume data.
        volume : float
            The volume of the volume data.
        existing_volume : dictionary
            The existing volume data with the same date as the current volume data.

        Returns:
        --------
        total_volume : list of dictionaries
            The total volume of all derivative constellium groups.
        """
        total_volume = []
        for data in self.derivative_constellium_group_dict_list:
            derivative_constellium_group_id = data['id']
            inter_obj = self.VolumeDerivativeIntermediateClass(
                derivative_constellium_group_id=derivative_constellium_group_id,
                search_date=self.search_date,
            )
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
