from backend.src.manager.part_sold_manager import PartSoldManager
from backend.src.intermediate.material_price_intermediate import MaterialPriceIntermediate
from backend.src.auxiliary.intermediate import GeneralIntermediate
from datetime import datetime, date

class PriceIntermediate(GeneralIntermediate):

    def __init__(
        self,
        part_sold_group_id: int,
        search_date: datetime | None = None,
        scenario_dict: dict = {},
    ):

        self.part_sold_group_id = part_sold_group_id
        self.scenario_dict = scenario_dict

        self.part_sold_manager = PartSoldManager(
            part_sold_group_id,
            search_date,
        )

        self.customer_manager = self.part_sold_manager.customer_manager
        self.material_price_intermediate = MaterialPriceIntermediate(
            self.customer_manager.customer_group_id,
            search_date,
            scenario_dict,
        )

        self.stock_exchange_data_manager = MaterialPriceIntermediate(
            search_date,
        )

        dependencies = [
            self.part_sold_manager,
            self.customer_manager,
            self.material_price_intermediate,
            self.stock_exchange_data_manager,
        ]

        self.super().__init__(
            search_date,
            scenario_dict,
            dependencies
        )

        self._price_component_development: list | None = None
        self._max_price_date: date
        self._min_price_date: date

    @property
    def current_price(self) -> float:
        current_date = date.now()
        return self.get_price(current_date)

    def get_price(self, date: date) -> float:
        if date > self._max_price_date:
            date = self._max_price_date
        elif date < self._min_price_date:
            date = self._min_price_date

        year_month = date.strftime("%Y-%m")
        for price_data in self.price_component_development:
            if price_data['date'] == year_month:
                return price_data

    @property
    def price_component_development(self) -> list:
        if self._price_component_development is None:
            self._price_component_development = self.__get_price_component_development()
        return self._price_component_development
    
    def __get_price_component_development(self) -> list:
        pass
