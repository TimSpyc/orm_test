if __name__ == '__main__':
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'orm_test.settings')

    import django
    django.setup()

from faker import Faker
import random
from datetime import date
from auxiliary import getRandomReference
from backend.models import CustomerGroup, Customer, CustomerMaterialCondition, PartSoldMaterialPriceType

fake = Faker()

def populateCustomer():
    group = fake.company()
    group_name = f'''
        {group} {random.choice(["AG", "Inc.", "Group", "Corp."])}
    '''
    company_name = fake.company()
    customer_group = CustomerGroup(
        company_name= company_name,
        group_name = group_name
    )
    customer_group.save()

    customer = Customer(
        customer_group = customer_group
    )
    customer.save()

    for part_sold_material_price_type in PartSoldMaterialPriceType.objects.all():
        if random.randint(0, 4) < 3:
            CustomerMaterialCondition(**{
                'customer': customer,
                'part_sold_material_price_type': part_sold_material_price_type,
                'month_range': random.randint(1, 24),
                'month_offset': random.choice(1, 3, 6, 9, 12, 18),
                'share_the_pain_factor': random.choice(random.randint(1, 10) / 10, 1, 1, 1),
                'validity_start_date': None,
                'validity_end_date': None
            }).save()
        else:
            start_date = fake.date_time_between_dates(
                datetime_start=date(2019, 1, 1),
                datetime_end=date(2023, 12, 31)
            )
            end_date = fake.date_time_between_dates(
                datetime_start=start_date,
                datetime_end=date(2032, 12, 31)
            )
            CustomerMaterialCondition(**{
                'customer': customer,
                'part_sold_material_price_type': part_sold_material_price_type,
                'month_range': random.randint(1, 24),
                'month_offset': [1, 3, 6, 9, 12, 18][random.randint(0, 5)],
                'share_the_pain_factor': random.choice(random.randint(1, 10) / 10, 1, 1, 1),
                'validity_start_date': None,
                'validity_end_date': start_date
            }).save()
            if random.randint(0, 3) < 3:
                continue
            CustomerMaterialCondition(**{
                'customer': customer,
                'part_sold_material_price_type': part_sold_material_price_type,
                'month_range': random.randint(1, 24),
                'month_offset': [1, 3, 6, 9, 12, 18][random.randint(0, 5)],
                'share_the_pain_factor': random.choice(random.randint(1, 10) / 10, 1, 1, 1),
                'validity_start_date': start_date,
                'validity_end_date': end_date
            }).save()
            if random.randint(0, 3) < 3:
                continue
            CustomerMaterialCondition(**{
                'customer': customer,
                'part_sold_material_price_type': part_sold_material_price_type,
                'month_range': random.randint(1, 24),
                'month_offset': [1, 3, 6, 9, 12, 18][random.randint(0, 5)],
                'share_the_pain_factor': random.choice(random.randint(1, 10) / 10, 1, 1, 1),
                'validity_start_date': start_date,
                'validity_end_date': None
            }).save()