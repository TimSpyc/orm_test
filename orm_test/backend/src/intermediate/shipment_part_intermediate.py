# Responsible Elias Bauer

from backend.src.intermediate import (
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

        self.shipment = self.getShipment()

        super().__init__(
            search_date,
            scenario_dict,
        )
    
    def getShipment(self):
        '''
        Description:
        ------------
        Calculates the shipment data based on the volume and current weight data.

        Returns:
        --------
        total_shipment : list
            A list of dictionaries containing the shipment data for each date.
        '''
        total_shipment = []
        
        for data in self.volume:
            date_item = {}
            date_item['shipment_data'] = data['volume_date']
            for category, value in self.current_weight.items():
                date_item[category] = value * data['volume']
            total_shipment.append(date_item)

        return total_shipment