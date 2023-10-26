from backend.src.manager.customer_manager import CustomerManager
from backend.src.manager.stock_exchange_manager import StockExchangeDataManager
from backend.src.auxiliary.intermediate import GeneralIntermediate
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from statistics import mean

class MaterialPriceIntermediate(GeneralIntermediate):
    relevant_scenario_keys = []

    def __init__(
        self,
        customer_group_id: int,
        search_date: datetime | None = None,
        scenario_dict: dict = {},
    ):

        self.customer_group_id = customer_group_id
        self.scenario_dict = scenario_dict

        self.customer_manager = CustomerManager(
            customer_group_id,
            search_date,
        )

        self.stock_exchange = StockExchangeDataManager(
            search_date,
        )

        dependencies = [self.customer_manager, self.stock_exchange]

        self.min_date = float('inf')
        self.max_date = float('-inf')
        self.price_development = self.calculatePriceDevelopment()

        self.super().__init__(
            search_date,
            scenario_dict,
            dependencies
        )

    @property
    def current_price(self) -> float:
        return self.getValidPrice(date.now())

    def getValidPrice(self, lookup_date: date | datetime) -> dict:
        is_datetime = isinstance(lookup_date, datetime)
        is_date = isinstance(lookup_date, date)
        if not is_datetime and not is_date:
            raise TypeError('''
                lookup_date must be of type datetime.date or datetime.datetime
            ''')

        year_month = lookup_date.year * 100 + lookup_date.month
        
        if year_month < self.min_date:
            return self.price_development[0]
        if year_month > self.max_date:
            return self.price_development[-1]

        for price_data in self.price_development:
            if price_data['year_month'] == year_month:
                return price_data

    def calculatePriceDevelopment(self) -> list:
        price_development = []
        
        for metal_price_data in self.stock_exchange.metal_cost_list_monthly:
            price_development_dict = {
                'year_month': metal_price_data['year_month'],
            }
            for type in ['lme', 'ecdp', 'billet_upcharge', 'billet']:
                material_price = self.__getCustomerMaterialPrice(
                    type,
                    metal_price_data['year_month']
                )
                if material_price is None:
                    break
                price_development_dict[type]

            self.__setDateBoundaries(metal_price_data['year_month'])

            if material_price is None:
                continue
            price_development.append(price_development_dict)
        
        return price_development

    def __setDateBoundaries(self, year_month: int) -> None:
        self.min_date = min(self.min_date, year_month)
        self.max_date = max(self.max_date, year_month)

    def __getCustomerMaterialPrice(
        self,
        type: str,
        year_month: float
    ) -> float:
        formula = self.__getPriceFormula(type, year_month)
        if formula is None:
            return None
        return self.__applyPriceFormula(formula, year_month)

    def __getPriceFormula(self, type: str, year_month: int) -> dict:
        lookup_date = date(year_month // 100, year_month % 100, 1)
        
        formula = filter(
            lambda x: (
                x['part_sold_material_price_type'] == type and
                (x['validity_start_date'] <= lookup_date or
                 x['validity_start_date'] is None) and
                (x['validity_end_date'] >= lookup_date or 
                 x['validity_end_date'] is None)
            ),
            self.customer_manager.customer_material_condition_dict_list
        )
        if len(formula) == 0:
            return None
        return formula[0]

    def __applyPriceFormula(
        self,
        formula: dict,
        year_month: float,
        type: str
    ) -> float:

        lookup_date = date(year_month // 100, year_month % 100, 1)

        month_range = formula['month_range']
        month_offset = formula['month_offset']
        share_the_pain_factor = formula['share_the_pain_factor']

        year_month_list = [
            lookup_date - relativedelta(months=(month_offset + i))
            for i in range(month_range)
        ]

        for year_month in year_month_list:
            lookup_date_check = date(year_month // 100, year_month % 100, 1)
            if not self.stock_exchange.isExistingDate(lookup_date_check):
                return None

        return mean(
            map(
                lambda x: x[type] * share_the_pain_factor,
                filter(
                    lambda x: x['year_month'] in [
                    date.year * 100 + date.month for date in year_month_list
                    ]
                ), self.stock_exchange.metal_cost_list_monthly
            )
        )

