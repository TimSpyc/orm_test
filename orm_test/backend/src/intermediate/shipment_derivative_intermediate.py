# Responsible Elias Bauer

from backend.src.intermediate import intermediate_auxiliary
from backend.src.manager import BillOfMaterialManager
from backend.src.intermediate.volumeLmc_derivativeConstellium_intermediate import VolumeLmcDerivativeConstelliumIntermediate
from backend.src.intermediate.volumeCustomer_derivativeConstellium_intermediate import VolumeCustomerDerivativeConstelliumIntermediate
from backend.src.intermediate.shipment_part_intermediate import ShipmentPartIntermediate
from backend.src.auxiliary.intermediate import GeneralIntermediate
import backend.src.auxiliary.list_of_dicts  as inter_lod
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
        self.search_date = search_date
        self.derivative_constellium_group_id = derivative_constellium_group_id
        
        self.volume = self.VolumeDerivativeIntermediateClass(
            derivative_constellium_group_id=self.derivative_constellium_group_id,
            search_date=search_date,
        ).volume
        
        self.head_node_list = BillOfMaterialManager.product_development_bom.head_node_list
        self.shipment, self.shipment_head_parts = self.getShipment()

        super().__init__(
            search_date,
            scenario_dict,
        )

    def getShipment(self):
        total_shipment = []
        shipment_head_parts = []
    
        for part_group_id in self.head_node_list:
            ship_part_obj = ShipmentPartIntermediate(
                part_group_id=part_group_id,
                search_date=self.search_date
            )
            part_der_shipment = ship_part_obj.getShipmentForDerivativeGroup(
                der_group_id=self.derivative_constellium_group_id
            )

            total_shipment += part_der_shipment
            shipment_head_parts.append({
                'part_group_id': part_group_id,
                'part_shipment_for_derivative': part_der_shipment
                })
        
        return inter_lod.groupListOfDictsByListOfStrings(
            result_list_dict=total_shipment,
            group_by_key_list=['date']
        ), shipment_head_parts