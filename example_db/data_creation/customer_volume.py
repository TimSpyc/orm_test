if __name__ == '__main__':
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'orm_test.settings')

    import django
    django.setup()

from faker import Faker
import random
from backend.models import CustomerVolumeGroup, CustomerVolume, CustomerVolumeVolume, ProjectPhaseType, DerivativeConstelliumGroup, User
from dateutil.relativedelta import relativedelta
from example_db.auxiliary import deactivateLastObjectRandomly, getRandomReference
from datetime import date, datetime

fake = Faker()

def populateCustomerVolume():

    derivative_constellium_group = getRandomReference(
        DerivativeConstelliumGroup
    )
    is_first_entry = len(list(CustomerVolumeGroup.objects.filter(
        DerivativeConstelliumGroup = derivative_constellium_group
    ))) == 0
    group_object = CustomerVolumeGroup(
        derivative_constellium_group=derivative_constellium_group
    )
    group_object.save()
    project_phase_type = getRandomReference(ProjectPhaseType)
    for _ in range(random.randint(1, 5)):
        sop_date = fake.date_time_between_dates(
                datetime_start=date(2019, 1, 1),
                datetime_end=date(2023, 12, 31)
            )
        eop_date = sop_date + relativedelta(sop_date, years=random.randint(3, 10))
        data_obj = CustomerVolume(
            volume_customer_group=group_object,
            project_phase_type=project_phase_type,
            sop=sop_date,
            eop=eop_date,
            date=datetime.now(),
            creator=getRandomReference(User),
            used_volume=is_first_entry
        )
        data_obj.save()
        
        total_volume = random.randint(100000, 1500000)
        year_divisor = eop_date.year - sop_date.year
        for year in range(sop_date.year, eop_date.year+1):
            volume = total_volume/year_divisor
            CustomerVolumeVolume(
                customer_volume=data_obj,
                volume=volume,
                volume_date=date(year, 1, 1),
            ).save()

    deactivateLastObjectRandomly(data_obj)