from backend.src.manager import PartSoldManager
from backend.src.intermediate.material_price_intermediate import MaterialPriceIntermediate
from backend.src.auxiliary.intermediate import GeneralIntermediate
from datetime import datetime, date

class BillOfMaterialIntermediate(GeneralIntermediate):
    relevant_scenario_keys = []

    def __init__(
        self,
        bill_of_material_group_id: int,
        search_date: datetime | None = None,
        scenario_dict: dict = {},
        use_cache: bool = True
    ):
        
        self.bill_of_material_group_id = bill_of_material_group_id
        self.scenario_dict = scenario_dict

        self.bill_of_material_manager = BillOfMaterialManager(
            bill_of_material_group_id,
            search_date,
            use_cache
        )

        self.bill_of_material_structure_manager_list = BillOfMaterialStructureManager(
            self.bill_of_material_manager.bill_of_material_group_id,
            search_date,
            use_cache
        )