from backend.src.manager.customer_manager import CustomerManager
from backend.src.manager.stock_exchange_manager import StockExchangeDataManager
from backend.src.auxiliary.intermediate import GeneralIntermediate
from datetime import datetime

class MaterialPriceIntermediate(GeneralIntermediate):
    relevant_scenario_keys = []

    def __init__(
        self,
        customer_group_id: int,
        search_date: datetime | None = None,
        scenario_dict: dict = {},
        use_cache: bool = True
    ):

        self.customer_group_id = customer_group_id
        self.scenario_dict = scenario_dict

        self.customer_manager = CustomerManager(
            customer_group_id,
            search_date,
            use_cache
        )

        self.stock_exchange_data_manager = StockExchangeDataManager(
            search_date,
            use_cache
        )

        dependencies = [self.customer_manager, self.stock_exchange_data_manager]

        self.super().__init__(
            search_date,
            scenario_dict,
            dependencies
        )

    @property
    def current_price(self):
        
    @property
    def price_development(self):
