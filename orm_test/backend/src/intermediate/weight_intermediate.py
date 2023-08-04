from backend.src.manager import PartManager
from backend.src.auxiliary.intermediate import GeneralIntermediate
from datetime import datetime, date

class WeightIntermediate(GeneralIntermediate):
    relevant_scenario_keys = []

    def __init__(
        self,
        part_group_id: int,
        search_date: datetime | None = None,
        scenario_dict: dict = {},
        use_cache: bool = True
    ):
        
    