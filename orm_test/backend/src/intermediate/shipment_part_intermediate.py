# Responsible Elias Bauer

from backend.src.intermediate import (
    auxiliary,
    WeightPartIntermediate,
    VolumePartIntermediate
)
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

        self.shipment = auxiliary.calculateShipment(
            volume_dict=self.volume,
            current_weight_dict=self.current_weight)

        super().__init__(
            search_date,
            scenario_dict,
        )
