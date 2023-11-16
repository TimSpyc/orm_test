from django.db import models
from backend.models import ExternalDataTable
from backend.src.auxiliary.manager import ExternalDataManager
from statistics import mean
from datetime import date, datetime

class StockExchangeData(ExternalDataTable):
    stock_exchange_date = models.DateTimeField()
    aluminum_cash_to_M_plus_1 = models.FloatField()
    aluminum_sett = models.FloatField()
    aluminum_cash_bid = models.FloatField()
    aluminum_cash_ask = models.FloatField()
    aluminum_3_months_bid = models.FloatField()
    aluminum_3_months_ask = models.FloatField()
    aluminum_dec_year_1_bid = models.FloatField()
    aluminum_dec_year_1_ask = models.FloatField()
    aluminum_dec_year_2_bid = models.FloatField()
    aluminum_dec_year_2_ask = models.FloatField()
    aluminum_dec_year_3_bid = models.FloatField()
    aluminum_dec_year_3_ask = models.FloatField()
    aluminum_stocks_mt = models.FloatField()
    copper_sett = models.FloatField()
    copper_cash_bid = models.FloatField()
    copper_cash_ask = models.FloatField()
    copper_3_months_bid = models.FloatField()
    copper_3_months_ask = models.FloatField()
    copper_stocks_mt = models.FloatField()
    zinc_sett = models.FloatField()
    nickel_sett = models.FloatField()
    aluminum_alloy_sett = models.FloatField()
    exchange_rate_ecb_eur_usd = models.FloatField()
    exchange_rate_ecb_eur_chf = models.FloatField()
    exchange_rate_ecb_eur_gbp = models.FloatField()
    exchange_rate_ecb_eur_aud = models.FloatField()
    exchange_rate_ecb_eur_czk = models.FloatField()
    exchange_rate_ecb_eur_jpy = models.FloatField()
    exchange_rate_ecb_usd_chf = models.FloatField()
    exchange_rate_ecb_gbp_usd = models.FloatField()
    exchange_rate_ecb_usd_czk = models.FloatField()
    exchange_rate_ecb_usd_cny = models.FloatField()
    exchange_rate_fwd_points_eur_usd_1M = models.FloatField()
    exchange_rate_fwd_points_eur_usd_2M = models.FloatField()
    exchange_rate_fwd_points_eur_usd_3M = models.FloatField()
    exchange_rate_fwd_points_usd_chf_1M = models.FloatField()
    exchange_rate_fwd_points_usd_chf_2M = models.FloatField()
    exchange_rate_fwd_points_usd_chf_3M = models.FloatField()
    exchange_rate_LME_eur_usd = models.FloatField()
    exchange_rate_LME_usd_gbp = models.FloatField()
    exchange_rate_LME_usd_jpy = models.FloatField()
    silver_usd_oz = models.FloatField()
    premium_rotterdam_p1020A_duty_paid_usd_t_low = models.FloatField()
    premium_rotterdam_p1020A_duty_paid_usd_t_avg = models.FloatField()
    premium_rotterdam_p1020A_duty_paid_usd_t_high = models.FloatField()
    premium_rotterdam_p1020A_duty_unpaid_usd_t_low = models.FloatField()
    premium_rotterdam_p1020A_duty_unpaid_usd_t_avg = models.FloatField()
    premium_rotterdam_p1020A_duty_unpaid_usd_t_high = models.FloatField()
    premium_european_billet_6063EC_duty_paid_usd_t_low = models.FloatField()
    premium_european_billet_6063EC_duty_paid_usd_t_avg = models.FloatField()
    premium_european_billet_6063EC_duty_paid_usd_t_high = models.FloatField()
    premium_us_midwest_duty_paid_usd_lb_low = models.FloatField()
    premium_us_midwest_duty_paid_usd_lb_avg = models.FloatField()
    premium_us_midwest_duty_paid_usd_lb_high = models.FloatField()
    premium_japan_P1020A_duty_paid_usd_t_low = models.FloatField()
    premium_japan_P1020A_duty_paid_usd_t_avg = models.FloatField()
    premium_japan_P1020A_duty_paid_usd_t_high = models.FloatField()
    stock_exchange_date = models.DateTimeField(unique=True)

    def __str__(self):
        return f"StockExchangeData from {self.stock_exchange_date}"
    
    def manager(self, search_date):
        return StockExchangeDataManager(self.id, search_date)
    

class StockExchangeDataManager(ExternalDataManager):
    database_model = StockExchangeData

    def __init__(self, search_date=None):
        super().__init__(search_date)

        self.lme_monthly = self.__getMonthlyValues('lme')
        self.ecdp_monthly = self.__getMonthlyValues('ecdp')
        self.billet_upcharge_monthly = self.__getMonthlyValues(
            'billet_upcharge'
        )
        self.metal_cost_list_monthly = self.__getMonthlyMetalCostList()


    def __getMonthlyValues(self, type: str) -> dict:
        types = {
            'lme': 'aluminum_cash_ask',
            'ecdp': 'premium_rotterdam_p1020A_duty_paid_usd_t_avg',
            'billet_upcharge':
                'premium_european_billet_6063EC_duty_paid_usd_t_avg'
        }
        exchange_rate = 'exchange_rate_ecb_eur_usd'
        if type not in types:
            raise ValueError(f"Invalid type '{type}'")
        
        metal_price_list_of_dict = self.getData(
            columns=[types[type], exchange_rate, 'stock_exchange_date']
        )
        monthly_metal_price_dict = {}

        for metal_price_dict in metal_price_list_of_dict:
            year = metal_price_dict['stock_exchange_date'].year
            month = metal_price_dict['stock_exchange_date'].month
            year_month = year * 100 + month
            if year_month not in monthly_metal_price_dict:
                monthly_metal_price_dict[year_month] = []
            if metal_price_dict['price'] is None:
                continue
            monthly_metal_price_dict[year_month].append(
                metal_price_dict['price'] / metal_price_dict['exchange_rate']
            )

        for year_month in monthly_metal_price_dict.keys():
            monthly_metal_price_dict[year_month] = mean(
                monthly_metal_price_dict[year_month]
            )
        
        return monthly_metal_price_dict
    

    def __getMonthlyMetalCostList(self) -> list:
        monthly_metal_cost_list = []
        for year_month in self.lme_monthly.keys():
            monthly_metal_cost_list.append({
                'year_month': year_month,
                'lme': self.lme_monthly[year_month],
                'ecdp': self.ecdp_monthly[year_month],
                'billet_upcharge': self.billet_upcharge_monthly[year_month],
                'billet': (
                    self.ecdp_monthly[year_month] +
                    self.billet_upcharge_monthly[year_month]
                )
            })
        
        return monthly_metal_cost_list
    
    def isExistingDate(lookup_date: datetime | date) -> bool:
        return StockExchangeData.objects.filter(
            stock_exchange_date=lookup_date
        ).exists()

    def currencyExchange(
        self,
        input_currency_abbr: str,
        output_currency_abbr: str,
        lookup_date: date
    ) -> float:
        
        if input_currency_abbr == output_currency_abbr:
            return 1.0

        exchange_rate = self.__getExchangeRate(
            input_currency_abbr,
            output_currency_abbr,
            lookup_date
        )
        if exchange_rate is not None:
            return exchange_rate
        
        exchange_rate = self.__getExchangeRate(
            output_currency_abbr,
            input_currency_abbr,
            lookup_date
        )
        if exchange_rate is not None:
            return 1/exchange_rate
        
        raise ValueError(
            f"Exchange rate from {input_currency_abbr} to "
            f"{output_currency_abbr} not found for {lookup_date}"
        )

    def __getExchangeRate(
        self,
        input_currency_abbr: str,
        output_currency_abbr: str,
        lookup_date: date
    ) -> float:
        col = f"exchange_rate_ecb_{output_currency_abbr}_{input_currency_abbr}"
        return self.getData(
            columns=[col],
            filters={
                'stock_exchange_date': lookup_date
            }
        )[0][col]