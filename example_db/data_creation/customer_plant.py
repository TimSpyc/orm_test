if __name__ == '__main__':
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'orm_test.settings')

    import django
    django.setup()

from faker import Faker
import random
from auxiliary import getRandomReference, deactivateLastObjectRandomly, getRandomUser, getRandomDateTime
from backend.models import CustomerPlantGroup, CustomerPlant, CustomerGroup, PartRecipientGroup

fake = Faker()

def populateCustomerPlant():
    customer_plant_group = CustomerPlantGroup(
        customer_group = getRandomReference(CustomerGroup),
        plant_name = fake.company()
    )
    customer_plant_group.save()

    customer_plant = CustomerPlant(**{
        "city": fake.city(),
        "address": fake.street_address(),
        "postcode": fake.postcode(),
        "country": fake.country(),
        "latitude": fake.latitude(),
        "longitude": fake.longitude(),
        "customer_plant_group": customer_plant_group,
        "creator": getRandomUser(),
        "date": getRandomDateTime()
    })
    
    customer_plant.save()
    for _ in range(random.randint(0, 5)):
        customer_plant.part_recipient_group.add(getRandomReference(PartRecipientGroup))
    customer_plant.save()

    deactivateLastObjectRandomly(customer_plant)