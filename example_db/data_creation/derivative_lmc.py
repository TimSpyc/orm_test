if __name__ == '__main__':
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'orm_test.settings')

    import django
    django.setup()

from faker import Faker
import random
from auxiliary import getRandomDateTime, modelCreationDict, randomLetters, getRandomReference
from backend.models import DerivativeLmcGroup, DerivativeLmc, RevisionLMC, CustomerGroup, CustomerPlantGroup
from datetime import date

fake = Faker()

def populateDerivativeLmc():
    def get_lmc_data(lmc_rev_date):
        local_make = getRandomReference(CustomerGroup)
        production_model = fake.bs()
        sop_date = getRandomDateTime(t_delta_days=10*365)
        eop_date = fake.date_time_between_dates(
            datetime_start=sop_date,
            datetime_end=date(2035, 12, 31)
        )
        facelift = fake.date_time_between_dates(
            datetime_start=sop_date,
            datetime_end=eop_date
        )
        return {
            "derivative_lmc_group": der_lmc_group,
            "revision_lmc": lmc_rev_date,
            "region": random.choice(['America', 'Asia', 'Africa', 'Western Europa', 'Eastern Europa']),
            "trade_region": random.choice(['America', 'Asia', 'Africa', 'Western Europa', 'Eastern Europa']),
            "country": fake.country(),
            "sales_group": random.choice(9*[local_make]+ [getRandomReference(CustomerGroup)]),
            "manufacturer": random.choice(9*[local_make]+ [getRandomReference(CustomerGroup)]),
            "local_make": local_make,
            "local_model_line": fake.bs(),
            "local_program_code": randomLetters(),
            "local_production_model": production_model,
            "global_make": random.choice(9*[local_make]+ [getRandomReference(CustomerGroup)]),
            "global_production_model": random.choice(9*[production_model]+ [fake.bs()]),
            "gvw": random.choice(['abc', 'efg', 'hij']),
            "platform": fake.bs(),
            "plant": getRandomReference(CustomerPlantGroup),
            "production_type": random.choice(['full', 'semi']),
            "vehicle_type": fake.bs(),
            "regional_size": fake.bs(),
            "regional_body_type": fake.bs(),
            "regional_status": fake.bs(),
            "global_size": fake.bs(),
            "global_body_type": fake.bs(),
            "global_status": fake.bs(),
            "sop_date": sop_date,
            "eop_date": eop_date,
            "next_facelift": facelift,
            "last_actual": getRandomDateTime(),
            "design_lead": random.choice(9*[local_make]+ [getRandomReference(CustomerGroup)]),
            "design_lead_location": fake.city(),
            "design_lead_country": fake.country(),
            "date": lmc_rev_date.revision_date,
            "creator_id": 1
        }

    lmc_model_code = fake.uuid4()
    der_lmc_group = DerivativeLmcGroup(
        lmc_full_code=f'{lmc_model_code}{randomLetters()}',
        lmc_model_code=lmc_model_code
    )
    der_lmc_group.save()

    all_lmc_revisions = RevisionLMC.objects.all()
    for lmc_rev_date in all_lmc_revisions:
        der_lmc = None
        if random.choice([True]+4*[False]):
            lmc_data = get_lmc_data(lmc_rev_date)
            der_lmc = DerivativeLmc(**modelCreationDict(lmc_data, DerivativeLmc, der_lmc_group, chance_for_no_change=0.9)).save()

    if der_lmc is None:
        lmc_data = get_lmc_data(lmc_rev_date)
        DerivativeLmc(**modelCreationDict(lmc_data, DerivativeLmc, der_lmc_group)).save()
