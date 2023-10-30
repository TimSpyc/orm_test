# Responsible Elias Bauer

from backend.src.intermediate import (
    WeightIntermediate,
    VolumeLmcDerivativeConstelliumIntermediate,
    VolumeCustomerDerivativeConstelliumIntermediate
)
from backend.src.auxiliary.intermediate import GeneralIntermediate
from datetime import datetime

class ShipmentPartIntermediate(GeneralIntermediate):
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
        
        self.volume = VolumeDerivativeIntermediateClass(
            part_group_id=part_group_id,
            VolumeDerivativeIntermediateClass=VolumeDerivativeIntermediateClass,
            search_date=search_date,
        ).volume
        
        self.current_weight = WeightIntermediate(
            part_group_id=part_group_id,
            search_date=search_date,
        ).currentWeight

        self.shipment = self.getShipment()

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
    
    def getShipment(self):
        total_shipment = []
        
        for data in self.volume:
            date_item = {}
            date_item['shipment_data'] = data['volume_date']
            for weight_category in self.current_weight:
                date_item[weight_category.key] = weight_category.value * data['volume']
            total_shipment.append(date_item)

        return total_shipment