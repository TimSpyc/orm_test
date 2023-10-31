# Responsible Elias Bauer

from backend.src.manager import PartManager, BillOfMaterialManager
from backend.src.intermediate import (
    auxiliary,
    VolumeLmcDerivativeConstelliumIntermediate,
    VolumeCustomerDerivativeConstelliumIntermediate
)
from backend.src.auxiliary.intermediate import GeneralIntermediate
from datetime import datetime

class VolumePartIntermediate(GeneralIntermediate):
    relevant_scenario_keys = []
    
    def __init__(
        self,
        part_group_id: int,
        VolumeDerivativeIntermediateClass: GeneralIntermediate,
        search_date: datetime | None = None,
        scenario_dict: dict = {},
    ):
        
        self.VolumeDerivativeIntermediateClass = VolumeDerivativeIntermediateClass
        auxiliary.checkValidityOfVolumeDerivativeIntermediateClass(
            attribute_name = self.VolumeDerivativeIntermediateClass,
            valid_classes = [
                VolumeLmcDerivativeConstelliumIntermediate,
                VolumeCustomerDerivativeConstelliumIntermediate
            ]
        )
        
        self.search_date = search_date

        self.part_manager = PartManager(
            group_id=part_group_id,
            search_date=self.search_date,
        )
        self.bom_manager_list = self.part_manager.bill_of_material_manager_list

        self.volume, self.volume_derivative = self.getVolume()

        super().__init__(
            search_date,
            scenario_dict,
        )
    
    def getVolume(self) -> tuple[list, list]:
        total_volume = []
        total_volume_derivative = []
        
        for bom_manager in self.bom_manager_list:
            
            cumulated_quantity = 0
            for data in bom_manager.bill_of_material_structure_dict_list:
                if data['part_group_id'] == self.part_manager.group_id:
                    cumulated_quantity += data['cumulated_quantity']

            der_group_id = bom_manager.derivative_constellium_group_id
            
            inter_obj = self.VolumeDerivativeIntermediateClass(
                derivative_constellium_group_id = der_group_id,
                search_date=self.search_date)
            
            total_volume_derivative.append(
                {
                    'derivative_constellium_group_id': der_group_id,
                    'volume_derivative': inter_obj.volume,
                    'cumulated_quantity': cumulated_quantity
                }
            )
            
            total_volume = self.__updateTotalVolume(total_volume, cumulated_quantity, inter_obj)
            
        return total_volume, total_volume_derivative

    def __updateTotalVolume(
        self,
        total_volume: list,
        cumulated_quantity: float,
        inter_obj: GeneralIntermediate
    ) -> list:
        """
        Description:
        ------------
        Updates the total volume of a given intermediate object
        by multiplying the volume of each date by the cumulated quantity.

        Inputs/Parameters:
        -------------------
        total_volume : list
            A list of dictionaries containing the volume data for each date.
        cumulated_quantity : float
            The cumulated quantity of the intermediate object.
        inter_obj : GeneralIntermediate
            The intermediate object containing the volume data.

        Returns:
        --------
        total_volume : list
            A list of dictionaries containing the
            updated volume data for each date.
        """
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
                        'volume': volume * cumulated_quantity,
                    })
            else:
                existing_volume['volume'] += volume * cumulated_quantity
        return total_volume
            