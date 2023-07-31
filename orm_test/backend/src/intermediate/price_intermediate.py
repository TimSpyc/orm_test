from backend.src.manager.part_sold_manager import PartSoldManager
from backend.src.manager.stock_exchange_manager import StockExchangeDataManager
from backend.src.auxiliary.intermediate import GeneralIntermediate

class PriceIntermediate(GeneralIntermediate):
    relevant_scenario_keys = []

    def __init__(
        self,
        part_sold_group_id,
        search_date=None,
        scenario_dict={},
        use_cache=True
    ):

        self.part_sold_group_id = part_sold_group_id
        self.scenario_dict = scenario_dict

        self.part_sold_manager = PartSoldManager(
            part_sold_group_id,
            search_date,
            use_cache
        )

        self.stock_exchange_data_manager = StockExchangeDataManager(
            search_date,
            use_cache
        )

        dependencies = [self.part_sold_manager, self.stock_exchange_data_manager]

        self.super().__init__(
            search_date,
            scenario_dict,
            dependencies
        )
