# Responsible Elias Bauer

from backend.src.intermediate import intermediate_auxiliary
from backend.src.intermediate.volume_part_intermediate import VolumePartIntermediate
from backend.src.intermediate.weight_part_intermediate import WeightPartIntermediate
from backend.src.auxiliary.intermediate import GeneralIntermediate
from datetime import datetime


class ShipmentPartIntermediate(GeneralIntermediate):
    relevant_scenario_keys = []

    def __init__(
        self,
        part_group_id: int,
        search_date: datetime | None = None,
        scenario_dict: dict = {},
    ):  
        
        self.volume = VolumePartIntermediate(
            part_group_id=part_group_id,
            search_date=search_date,
        ).volume
        
        self.current_weight = WeightPartIntermediate(
            part_group_id=part_group_id,
            search_date=search_date,
        ).current_weight

        self.shipment = intermediate_auxiliary.calculateResultBasedOnVolume(
            volume_dict=self.volume,
            category_value_dict=self.current_weight)

        super().__init__(
            search_date,
            scenario_dict,
        )
