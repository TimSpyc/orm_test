from backend.src.auxiliary.intermediate import GeneralIntermediate
from datetime import datetime
from backend.src.manager.bill_of_material_manager import BillOfMaterialManager
from backend.src.manager.part_manager import PartManager
from backend.src.intermediate.weight_part_intermediate import WeightPartIntermediate

class BillOfMaterialPartIntermediate(GeneralIntermediate):
    relevant_scenario_keys = []

    def __init__(
        self,
        bill_of_material_group_id: int,
        search_date: datetime | None = None,
        scenario_dict: dict = {},
    ):
        self.bill_of_material_manager = BillOfMaterialManager(
            group_id=bill_of_material_group_id,
            search_date=search_date,
        )
    
        self.bill_of_material_detail_dict_list = self.createFilledBillOfMaterial()

        self.super().__init__(
            search_date,
            scenario_dict,
        )

    def createFilledBillOfMaterial(self):
        bill_of_material_detail_dict_list = []
        for bom_position in self.bill_of_material_manager.product_development_bom:
            part_manager = PartManager(bom_position["group_id"])
            part_weight_intermediate = WeightPartIntermediate(part_manager.group_id)
            bill_of_material_detail_dict_list.append({
                **bom_position,
                **dict(part_manager),
                "alu_gross_weight": part_weight_intermediate.alu_gross_weight,
                "alu_net_weight": part_weight_intermediate.alu_net_weight,
                "steel_gross_weight": part_weight_intermediate.steel_gross_weight,
                "steel_net_weight": part_weight_intermediate.steel_net_weight,
                "other_gross_weight": part_weight_intermediate.other_gross_weight,
                "other_net_weight": part_weight_intermediate.other_net_weight,
            })
        return bill_of_material_detail_dict_list


        