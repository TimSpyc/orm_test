from backend.src.manager.part_sold_manager import PartSoldManager
from backend.src.intermediate.material_price_intermediate import MaterialPriceIntermediate
from backend.src.auxiliary.intermediate import GeneralIntermediate
from datetime import datetime, date

class PriceIntermediate(GeneralIntermediate):
    relevant_scenario_keys = []

    def __init__(
        self,
        part_sold_group_id: int,
        search_date: datetime | None = None,
        scenario_dict: dict = {},
        use_cache: bool = True
    ):

        self.part_sold_group_id = part_sold_group_id
        self.scenario_dict = scenario_dict

        self.part_sold_manager = PartSoldManager(
            part_sold_group_id,
            search_date,
            use_cache
        )

        self.customer_manager = self.part_sold_manager.customer_manager
        self.material_price_intermediate = MaterialPriceIntermediate(
            self.customer_manager.customer_group_id,
            search_date,
            scenario_dict,
            use_cache
        )

        self.stock_exchange_data_manager = MaterialPriceIntermediate(
            search_date,
            use_cache
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

        self._price_component_development = None
        self._max_price_date: date | None = None
        self._min_price_date: date | None = None

    @property
    def current_price(self) -> float:
        current_date = date.now()
        return self.get_price(current_date)

    def get_price(self, date: date) -> float:
        if date > self.max_price_date:
            date = self.max_price_date
        elif date < self.min_price_date:
            date = self.min_price_date

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
        basis_price = self.__getBasePrice()
        material_price_information = self.__getMaterialPriceInformation()
        stock_exchange_price_list = self.__getStockExchangePrice()
        price_saving_information = self.__getPriceSavingInformation()
        return self.__calculatePriceComponentDevelopment(
            basis_price,
            material_price_information,
            stock_exchange_price_list,
            price_saving_information
        )

    def __calculatePriceComponentDevelopment(
        self,
        basis_price: dict,
        material_price_information: dict,
        stock_exchange_price_list: list,
        price_saving_information: dict
    ) -> list:
        price_component_development = []
        for stock_exchange_price in stock_exchange_price_list:
            date = stock_exchange_price['date']

            material_price_dict = self.__calculateMaterialCost(
                date,
                stock_exchange_price_list,
                material_price_information
            )

            price_component_development.append({
                'date': date,
                
            })
        return price_component_development