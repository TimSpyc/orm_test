from django.db import models
from backend.models import ExternalDataTable
from backend.src.auxiliary.manager import ExternalDataManager

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
    
    def manager(self, search_date, use_cache):
        return StockExchangeDataManager(self.id, search_date, use_cache)
    

class StockExchangeDataManager(ExternalDataManager):
    database_model = StockExchangeData

    def __init__(self, search_date=None):
        super().__init__(search_date)