from backend.src.auxiliary.info import GeneralInfo, addPrefix
from backend.src.manager import BillOfMaterialManager
from backend.src.manager.bill_of_material_manager import BillOfMaterialManager
from backend.src.manager.part_manager import PartManager
from backend.src.intermediate import WeightPartIntermediate


def __createFilledBillOfMaterial(manager_object):
    bill_of_material_detail_dict_list = []
    for bom_position in manager_object.product_development_bom:
        part_manager = PartManager(bom_position["group_id"])
        part_weight_intermediate = WeightPartIntermediate(part_manager.group_id)
        bill_of_material_detail_dict_list.append({
            **bom_position,
            **addPrefix("part", dict(part_manager)),
            "weight_part__alu_gross_weight": part_weight_intermediate.alu_gross_weight,
            "weight_part__alu_net_weight": part_weight_intermediate.alu_net_weight,
            "weight_part__steel_gross_weight": part_weight_intermediate.steel_gross_weight,
            "weight_part__steel_net_weight": part_weight_intermediate.steel_net_weight,
            "weight_part__other_gross_weight": part_weight_intermediate.other_gross_weight,
            "weight_part__other_net_weight": part_weight_intermediate.other_net_weight,
        })
    return bill_of_material_detail_dict_list

class BillOfMaterialInfo(GeneralInfo):
    base_url = 'bill_of_material'
    allowed_method_list = ['GET_detail', 'GET_list', 'DELETE']
    required_permission_list = []
    manager = BillOfMaterialManager
    serializerFunction = lambda manager_object: (
        __createFilledBillOfMaterial(manager_object)
    )

