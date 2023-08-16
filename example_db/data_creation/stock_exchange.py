if __name__ == '__main__':
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'orm_test.settings')

    import django
    django.setup()

from faker import Faker
import random
from auxiliary import getRandomDateTime, getRandomUser, deactivateLastObjectRandomly
from backend.models import StockExchangeData
from datetime import datetime, timedelta

fake = Faker()

def populateStockExchangeData():
    start_date = fake.date_between(start_date='-10y', end_date='today')
    end_date = datetime.now()
    date = start_date
    aluminum_cash_to_M_plus_1 = random.uniform(1000, 5000)
    copper_sett = random.uniform(1000, 5000)
    zinc_sett = random.uniform(1000, 5000)
    nickel_sett = random.uniform(1000, 5000)
    aluminum_alloy_sett = random.uniform(1000, 5000)
    silver_usd_oz = random.uniform(10, 50)

    exchange_rate_ecb_eur_usd = random.uniform(0.8, 1.5)
    exchange_rate_ecb_eur_chf = random.uniform(0.8, 1.5)
    exchange_rate_ecb_eur_gbp = random.uniform(0.8, 1.5)
    exchange_rate_ecb_eur_aud = random.uniform(0.8, 1.5)
    exchange_rate_ecb_eur_czk = random.uniform(20, 40)
    exchange_rate_ecb_eur_jpy = random.uniform(80, 150)

    premium_rotterdam_p1020A_duty_paid_usd_t_avg = random.uniform(100, 500)
    premium_rotterdam_p1020A_duty_unpaid_usd_t_avg = random.uniform(100, 500)
    premium_european_billet_6063EC_duty_paid_usd_t_avg = random.uniform(100, 500) + premium_rotterdam_p1020A_duty_paid_usd_t_avg
    premium_us_midwest_duty_paid_usd_lb_avg = random.uniform(100, 500) + premium_rotterdam_p1020A_duty_paid_usd_t_avg
    premium_japan_P1020A_duty_paid_usd_t_avg = random.uniform(100, 500) + premium_rotterdam_p1020A_duty_paid_usd_t_avg

    while date < end_date:
        date += timedelta(days=1)

        aluminum_cash_to_M_plus_1 *= random.uniform(0.98, 1.02)
        aluminum_sett = aluminum_cash_to_M_plus_1 * random.uniform(0.98, 1.02)
        aluminum_cash_bid = aluminum_cash_to_M_plus_1 * random.uniform(0.98, 1.02)
        aluminum_cash_ask = aluminum_cash_to_M_plus_1 * random.uniform(0.98, 1.02)
        aluminum_3_months_bid = aluminum_cash_to_M_plus_1 * random.uniform(0.95, 1.05)
        aluminum_3_months_ask = aluminum_3_months_bid * random.uniform(0.95, 1.05)
        aluminum_dec_year_1_bid = aluminum_3_months_bid * random.uniform(0.95, 1.05)
        aluminum_dec_year_1_ask = aluminum_dec_year_1_bid * random.uniform(0.95, 1.05)
        aluminum_dec_year_2_bid = aluminum_dec_year_1_bid * random.uniform(0.95, 1.05)
        aluminum_dec_year_2_ask = aluminum_dec_year_2_bid * random.uniform(0.95, 1.05)
        aluminum_dec_year_3_bid = aluminum_dec_year_2_bid * random.uniform(0.95, 1.05)
        aluminum_dec_year_3_ask = aluminum_dec_year_3_bid * random.uniform(0.95, 1.05)
        aluminum_stocks_mt = random.uniform(100000, 1000000)
        copper_sett *= random.uniform(0.98, 1.02)
        copper_cash_bid = copper_sett * random.uniform(0.98, 1.02)
        copper_cash_ask = copper_sett * random.uniform(0.98, 1.02)
        copper_3_months_bid = copper_sett * random.uniform(0.95, 1.05)
        copper_3_months_ask = copper_3_months_bid * random.uniform(0.95, 1.05)
        copper_stocks_mt = random.uniform(100000, 1000000)
        zinc_sett *= random.uniform(0.98, 1.02)
        nickel_sett *= random.uniform(0.98, 1.02)
        aluminum_alloy_sett *= random.uniform(0.98, 1.02)
        exchange_rate_ecb_eur_usd *= random.uniform(0.98, 1.02)
        exchange_rate_ecb_eur_chf *= random.uniform(0.98, 1.02)
        exchange_rate_ecb_eur_gbp *= random.uniform(0.98, 1.02)
        exchange_rate_ecb_eur_aud *= random.uniform(0.98, 1.02)
        exchange_rate_ecb_eur_czk *= random.uniform(0.98, 1.02)
        exchange_rate_ecb_eur_jpy *= random.uniform(0.98, 1.02)
        exchange_rate_ecb_usd_chf = exchange_rate_ecb_eur_usd / exchange_rate_ecb_eur_chf
        exchange_rate_ecb_gbp_usd = exchange_rate_ecb_eur_usd / exchange_rate_ecb_eur_gbp
        exchange_rate_ecb_usd_czk = exchange_rate_ecb_eur_usd / exchange_rate_ecb_eur_czk
        exchange_rate_ecb_usd_cny = exchange_rate_ecb_eur_usd / exchange_rate_ecb_eur_jpy
        exchange_rate_fwd_points_eur_usd_1M = random.uniform(-0.5, 0.5)
        exchange_rate_fwd_points_eur_usd_2M = random.uniform(-0.5, 0.5)
        exchange_rate_fwd_points_eur_usd_3M = random.uniform(-0.5, 0.5)
        exchange_rate_fwd_points_usd_chf_1M = random.uniform(-0.5, 0.5)
        exchange_rate_fwd_points_usd_chf_2M = random.uniform(-0.5, 0.5)
        exchange_rate_fwd_points_usd_chf_3M = random.uniform(-0.5, 0.5)
        exchange_rate_LME_eur_usd = exchange_rate_ecb_eur_usd
        exchange_rate_LME_usd_gbp = 1/exchange_rate_ecb_gbp_usd
        exchange_rate_LME_usd_jpy = exchange_rate_ecb_usd_cny
        silver_usd_oz *= random.uniform(0.98, 1.02)
        premium_rotterdam_p1020A_duty_paid_usd_t_avg *= random.uniform(0.98, 1.02)
        premium_rotterdam_p1020A_duty_unpaid_usd_t_avg *= random.uniform(0.98, 1.02)
        premium_european_billet_6063EC_duty_paid_usd_t_avg *= random.uniform(0.98, 1.02)
        premium_us_midwest_duty_paid_usd_lb_avg *= random.uniform(0.98, 1.02)
        premium_japan_P1020A_duty_paid_usd_t_avg *= random.uniform(0.98, 1.02)
        premium_rotterdam_p1020A_duty_paid_usd_t_low = premium_rotterdam_p1020A_duty_paid_usd_t_avg * random.uniform(0.90, 0.99)
        premium_rotterdam_p1020A_duty_paid_usd_t_high = premium_rotterdam_p1020A_duty_paid_usd_t_avg * random.uniform(1.01, 1.10)
        premium_rotterdam_p1020A_duty_unpaid_usd_t_low = premium_rotterdam_p1020A_duty_unpaid_usd_t_avg * random.uniform(0.90, 0.99)
        premium_rotterdam_p1020A_duty_unpaid_usd_t_high = premium_rotterdam_p1020A_duty_unpaid_usd_t_avg * random.uniform(1.01, 1.10)
        premium_european_billet_6063EC_duty_paid_usd_t_low = premium_european_billet_6063EC_duty_paid_usd_t_avg * random.uniform(0.90, 0.99)
        premium_european_billet_6063EC_duty_paid_usd_t_high = premium_european_billet_6063EC_duty_paid_usd_t_avg * random.uniform(1.01, 1.10)
        premium_us_midwest_duty_paid_usd_lb_low = premium_us_midwest_duty_paid_usd_lb_avg * random.uniform(0.90, 0.99)
        premium_us_midwest_duty_paid_usd_lb_high = premium_us_midwest_duty_paid_usd_lb_avg * random.uniform(1.01, 1.10)
        premium_japan_P1020A_duty_paid_usd_t_low = premium_japan_P1020A_duty_paid_usd_t_avg * random.uniform(0.90, 0.99)
        premium_japan_P1020A_duty_paid_usd_t_high = premium_japan_P1020A_duty_paid_usd_t_avg * random.uniform(1.01, 1.10)
        stock_exchange_date = date

        stock_exchange_data = StockExchangeData(
            aluminum_cash_to_M_plus_1 = aluminum_cash_to_M_plus_1,
            aluminum_sett = aluminum_sett,
            aluminum_cash_bid = aluminum_cash_bid,
            aluminum_cash_ask = aluminum_cash_ask,
            aluminum_3_months_bid = aluminum_3_months_bid,
            aluminum_3_months_ask = aluminum_3_months_ask,
            aluminum_dec_year_1_bid = aluminum_dec_year_1_bid,
            aluminum_dec_year_1_ask = aluminum_dec_year_1_ask,
            aluminum_dec_year_2_bid = aluminum_dec_year_2_bid,
            aluminum_dec_year_2_ask = aluminum_dec_year_2_ask,
            aluminum_dec_year_3_bid = aluminum_dec_year_3_bid,
            aluminum_dec_year_3_ask = aluminum_dec_year_3_ask,
            aluminum_stocks_mt = aluminum_stocks_mt,
            copper_sett = copper_sett,
            copper_cash_bid = copper_cash_bid,
            copper_cash_ask = copper_cash_ask,
            copper_3_months_bid = copper_3_months_bid,
            copper_3_months_ask = copper_3_months_ask,
            copper_stocks_mt = copper_stocks_mt,
            zinc_sett = zinc_sett,
            nickel_sett = nickel_sett,
            aluminum_alloy_sett = aluminum_alloy_sett,
            exchange_rate_ecb_eur_usd = exchange_rate_ecb_eur_usd,
            exchange_rate_ecb_eur_chf = exchange_rate_ecb_eur_chf,
            exchange_rate_ecb_eur_gbp = exchange_rate_ecb_eur_gbp,
            exchange_rate_ecb_eur_aud = exchange_rate_ecb_eur_aud,
            exchange_rate_ecb_eur_czk = exchange_rate_ecb_eur_czk,
            exchange_rate_ecb_eur_jpy = exchange_rate_ecb_eur_jpy,
            exchange_rate_ecb_usd_chf = exchange_rate_ecb_usd_chf,
            exchange_rate_ecb_gbp_usd = exchange_rate_ecb_gbp_usd,
            exchange_rate_ecb_usd_czk = exchange_rate_ecb_usd_czk,
            exchange_rate_ecb_usd_cny = exchange_rate_ecb_usd_cny,
            exchange_rate_fwd_points_eur_usd_1M = exchange_rate_fwd_points_eur_usd_1M,
            exchange_rate_fwd_points_eur_usd_2M = exchange_rate_fwd_points_eur_usd_2M,
            exchange_rate_fwd_points_eur_usd_3M = exchange_rate_fwd_points_eur_usd_3M,
            exchange_rate_fwd_points_usd_chf_1M = exchange_rate_fwd_points_usd_chf_1M,
            exchange_rate_fwd_points_usd_chf_2M = exchange_rate_fwd_points_usd_chf_2M,
            exchange_rate_fwd_points_usd_chf_3M = exchange_rate_fwd_points_usd_chf_3M,
            exchange_rate_LME_eur_usd = exchange_rate_LME_eur_usd,
            exchange_rate_LME_usd_gbp = exchange_rate_LME_usd_gbp,
            exchange_rate_LME_usd_jpy = exchange_rate_LME_usd_jpy,
            silver_usd_oz = silver_usd_oz,
            premium_rotterdam_p1020A_duty_paid_usd_t_low = premium_rotterdam_p1020A_duty_paid_usd_t_low,
            premium_rotterdam_p1020A_duty_paid_usd_t_avg = premium_rotterdam_p1020A_duty_paid_usd_t_avg,
            premium_rotterdam_p1020A_duty_paid_usd_t_high = premium_rotterdam_p1020A_duty_paid_usd_t_high,
            premium_rotterdam_p1020A_duty_unpaid_usd_t_low = premium_rotterdam_p1020A_duty_unpaid_usd_t_low,
            premium_rotterdam_p1020A_duty_unpaid_usd_t_avg = premium_rotterdam_p1020A_duty_unpaid_usd_t_avg,
            premium_rotterdam_p1020A_duty_unpaid_usd_t_high = premium_rotterdam_p1020A_duty_unpaid_usd_t_high,
            premium_european_billet_6063EC_duty_paid_usd_t_low = premium_european_billet_6063EC_duty_paid_usd_t_low,
            premium_european_billet_6063EC_duty_paid_usd_t_avg = premium_european_billet_6063EC_duty_paid_usd_t_avg,
            premium_european_billet_6063EC_duty_paid_usd_t_high = premium_european_billet_6063EC_duty_paid_usd_t_high,
            premium_us_midwest_duty_paid_usd_lb_low = premium_us_midwest_duty_paid_usd_lb_low,
            premium_us_midwest_duty_paid_usd_lb_avg = premium_us_midwest_duty_paid_usd_lb_avg,
            premium_us_midwest_duty_paid_usd_lb_high = premium_us_midwest_duty_paid_usd_lb_high,
            premium_japan_P1020A_duty_paid_usd_t_low = premium_japan_P1020A_duty_paid_usd_t_low,
            premium_japan_P1020A_duty_paid_usd_t_avg = premium_japan_P1020A_duty_paid_usd_t_avg,
            premium_japan_P1020A_duty_paid_usd_t_high = premium_japan_P1020A_duty_paid_usd_t_high,
            stock_exchange_date = stock_exchange_date
        )

        stock_exchange_data.save()
