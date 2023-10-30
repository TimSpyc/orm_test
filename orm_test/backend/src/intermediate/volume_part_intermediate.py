# Responsible Elias Bauer

from backend.src.manager import PartManager, BillOfMaterialManager
from backend.src.intermediate import (
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
        self.__checkValidityOfVolumeDerivativeIntermediateClass(
            VolumeDerivativeIntermediateClass
        )
        
        self.search_date = search_date

        self.part_manager = PartManager(
            group_id=part_group_id,
            search_date=self.search_date,
        )
        self.bom_manager_list = self.part_manager.bill_of_material_manager_list

        self.volume, self.volume_derivative = self.getVolume(VolumeDerivativeIntermediateClass)

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
    
    def getVolume(self, VolumeDerivativeIntermediateClass: GeneralIntermediate):
        total_volume = []
        total_volume_derivative = []
        
        for bom_manager in self.bom_manager_list:
            bom_data_dict = bom_manager.getBillOfMaterialDetails(
                'product_development',
                head_part_group_id=self.part_manager.group_id
            )
            relative_quantity = bom_data_dict['head_node']['relative_quantity']
            der_group_id = bom_manager.derivative_constellium_group_id
            
            inter_obj = VolumeDerivativeIntermediateClass(
                derivative_constellium_group_id = der_group_id,
                search_date=self.search_date)
            
            total_volume_derivative.append(
                {
                    'derivative_constellium_group_id': der_group_id,
                    'volume_derivative': inter_obj.volume,
                    'takerate': relative_quantity
                }
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
                        'volume': volume * relative_quantity,
                    })
                else:
                    existing_volume['volume'] += volume * relative_quantity
            
        return total_volume, total_volume_derivative
            