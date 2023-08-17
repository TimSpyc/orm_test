if __name__ == '__main__':
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'orm_test.settings')

    import django
    django.setup()

from faker import Faker
import random
from auxiliary import getRandomReference, deactivateLastObjectRandomly, getRandomUser, getRandomDateTime
from backend.models import PartSoldCustomerPrice, PartSoldCustomerPriceGroup, PartSoldCustomerPriceComponent, PartSoldPriceComponentType, PartSoldGroup

fake = Faker()

def populatePartSoldCustomerPrice():

    part_sold_customer_price_group = PartSoldCustomerPriceGroup(
        part_sold_group = getRandomReference(PartSoldGroup),
        price_date = fake.date_time_between(start_date='-1y', end_date='now', tzinfo=None)
    )
    part_sold_customer_price_group.save()

    part_sold_customer_price = PartSoldCustomerPrice(
        part_sold_customer_price_group = part_sold_customer_price_group,
    )
    part_sold_customer_price.save()

    for _ in range(random.randint(1, 5)):
        part_sold_price_component = PartSoldCustomerPriceComponent(
            part_sold_customer_price = part_sold_customer_price,
            part_sold_price_component_type = getRandomReference(PartSoldPriceComponentType),
            value = fake.pyfloat(left_digits=2, right_digits=2, positive=True),
            creator = getRandomUser(),
            date = getRandomDateTime()
        )

        part_sold_price_component.save()

    deactivateLastObjectRandomly(part_sold_customer_price)