if __name__ == '__main__':
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'orm_test.settings')

    import django
    django.setup()

from faker import Faker
import random
from backend.models import DerivativeLmcGroup, DerivativeLmc, RevisionLMC, DerivativeLmcVolume
from dateutil.relativedelta import relativedelta
from example_db.auxiliary import deactivateLastObjectRandomly
from datetime import date

fake = Faker()

def populateVolumeForAllDerivativeLmc():
    all_object = DerivativeLmcGroup.objects.all()
    for der_lmc_group in all_object:
        populateLmcVolume(der_lmc_group)

def populateLmcVolume(derivative_lmc_group_model):
    der_lmc_obj = DerivativeLmc.objects.filter(derivative_lmc_group= derivative_lmc_group_model).latest('date')
    sop_date = der_lmc_obj.sop_date
    eop_date = der_lmc_obj.eop_date

    all_lmc_revisions = RevisionLMC.objects.all()
    date_delta = relativedelta(sop_date, eop_date)
    start_date = date(sop_date.year, sop_date.month, 1)
    total_month = date_delta.years*12 + date_delta.months
    standard_peak_volume = random.randint(200, 25000)


    for lmc_rev_date in all_lmc_revisions:
        use_lmc_rev =random.choice([True]+4*[False])
        peak_volume = standard_peak_volume * (1+random.randint(-20, 20)/100)
        volume = peak_volume
        for distance_sop_month in range(1, total_month+1):
            if distance_sop_month < total_month/3:
                volume = peak_volume *(1 - 0.9**distance_sop_month)
            elif distance_sop_month > total_month/3 and distance_sop_month < total_month/2.8:
                volume = peak_volume
            elif distance_sop_month <= total_month -total_month/5:
                volume -= 0.035*volume
            else:
                volume -= 0.1*volume

            insert_date = start_date + relativedelta(months=distance_sop_month)

            if use_lmc_rev:
                try:
                    DerivativeLmcVolume.objects.create(
                        derivative_lmc_group = derivative_lmc_group_model,
                        volume = int(volume),
                        date = insert_date,
                        lmc_revision = lmc_rev_date,
                    )
                except:
                    pass
    
    deactivateLastObjectRandomly(der_lmc_obj)

if __name__ == '__main__':
    populateVolumeForAllDerivativeLmc()