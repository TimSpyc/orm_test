from backend.src.auxiliary.info import GeneralInfo
from backend.src.manager import BillOfMaterialManager
from backend.src.intermediate import BillOfMaterialPartIntermediate

class BillOfMaterialInfo(GeneralInfo):
    base_url = 'bill_of_material'
    allowed_method_list = ['GET_detail', 'GET_list', 'DELETE']
    required_permission_list = []
    manager = BillOfMaterialManager
    serializerFunction = lambda intermediate_object: (
        intermediate_object.bill_of_material_detail_dict_list
    )

    def getDetail(self) -> BillOfMaterialPartIntermediate:
        bill_of_material_group_id = self.identifier.get("group_id")
        search_date = self.request_info_dict["query_params"].get(
            "search_date", None
        )

        return BillOfMaterialPartIntermediate(**{
            "bill_of_material_group_id": bill_of_material_group_id,
            "search_date": search_date,
        })
    
    def getList(self) -> list[BillOfMaterialPartIntermediate]:
        search_date = self.request_info_dict["query_params"].get(
            "search_date", None
        )
        return [
            BillOfMaterialPartIntermediate(manager_object.group_id)
            for manager_object in BillOfMaterialManager.all(search_date)
        ]