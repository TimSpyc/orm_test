# Responsible Elias Bauer

from backend.src.intermediate import intermediate_auxiliary
from backend.src.intermediate.volumeLmc_derivativeConstellium_intermediate import VolumeLmcDerivativeConstelliumIntermediate
from backend.src.intermediate.volumeCustomer_derivativeConstellium_intermediate import VolumeCustomerDerivativeConstelliumIntermediate
from backend.src.auxiliary.intermediate import GeneralIntermediate
from datetime import datetime

class ShipmentDerivativeIntermediate(GeneralIntermediate):
    relevant_scenario_keys = []
    
    def __init__(
        self,
        derivative_constellium_group_id: int,
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

        
        self.volume = self.VolumeDerivativeIntermediateClass(
            derivative_constellium_group_id=derivative_constellium_group_id,
            search_date=search_date,
        ).volume
        
        self.current_weight_list = self.getCurrentWeightList()
        # Only the first one
        # self.current_weight = WeightPartIntermediate(
        #     part_group_id=part_group_id,
        #     search_date=search_date,
        # ).current_weight

        #loop through this
        self.shipment = self.getShipment()

        super().__init__(
            search_date,
            scenario_dict,
        )

    def getCurrentWeightList(self):
        pass
    
# auxiliary.calculateShipment(
#             volume_dict=self.volume,
#             current_weight_dict=self.current_weight)
    def getShipment(self):
        total_shipment = []
        return total_shipment