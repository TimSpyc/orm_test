# Responsible Elias Bauer

from backend.src.intermediate import intermediate_auxiliary
from backend.src.intermediate.volumeLmc_derivativeConstellium_intermediate import VolumeLmcDerivativeConstelliumIntermediate
from backend.src.intermediate.volumeCustomer_derivativeConstellium_intermediate import VolumeCustomerDerivativeConstelliumIntermediate
from backend.src.intermediate.volume_part_intermediate import VolumePartIntermediate
from backend.src.intermediate.weight_part_intermediate import WeightPartIntermediate
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

        self.VolumeDerivativeIntermediateClass = VolumeDerivativeIntermediateClass
        intermediate_auxiliary.checkValidityOfVolumeDerivativeIntermediateClass(
            attribute_name = self.VolumeDerivativeIntermediateClass,
            valid_classes = [
                VolumeLmcDerivativeConstelliumIntermediate,
                VolumeCustomerDerivativeConstelliumIntermediate
            ]
        )
        self.search_date = search_date

        self.volume = VolumePartIntermediate(
            part_group_id=part_group_id,
            VolumeDerivativeIntermediateClass=self.VolumeDerivativeIntermediateClass,
            search_date=self.search_date,
        ).volume
        
        self.current_weight = WeightPartIntermediate(
            part_group_id=part_group_id,
            search_date=search_date,
        ).current_weight

        self.shipment = intermediate_auxiliary.calculateCategoryDictBasedOnVolume(
            volume_dict=self.volume,
            category_value_dict=self.current_weight)

        super().__init__(
            search_date,
            scenario_dict,
        )
    
    def getShipmentForDerivativeGroup(self, der_group_id: int) -> list[dict]:
        '''
        Description:
        --------
        This function calculates the shipment for a specific derivative group.

        Inputs/Parameters:
        --------
        der_group_id : int
            The ID of the derivative group for which the shipment is calculated.

        Returns:
        --------
        list[dict] : list of dictionaries
            A list of dictionaries, each with a 'date' key and
            additional keys for each category[weight-category], where the value
            is the product of the volume and the category value.
        '''
        der_volume = self.VolumeDerivativeIntermediateClass(
            derivative_constellium_group_id=der_group_id,
            VolumeDerivativeIntermediateClass=self.VolumeDerivativeIntermediateClass,
            search_date=self.search_date,
        ).volume

        return intermediate_auxiliary.calculateCategoryDictBasedOnVolume(
            volume_dict=der_volume,
            category_value_dict=self.current_weight)
