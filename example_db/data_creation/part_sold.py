if __name__ == '__main__':
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'orm_test.settings')

    import django
    django.setup()

from faker import Faker
import random
from auxiliary import getRandomReference, deactivateLastObjectRandomly, getRandomUser, getRandomDateTime
from backend.models import (
    PartSold,
    PartSoldGroup,
    PartSoldPriceComponent,
    PartSoldMaterialPriceComponent,
    PartSoldMaterialWeight,
    PartSoldSaving,
    PartRecipientGroup,
    SapNumber,
    CustomerGroup,
    PartSoldContractGroup,
    Currency,
    PartSoldPriceComponentType,
    PartSoldMaterialPriceType,
    MaterialType,
    SavingUnit
)

fake = Faker()

def populatePartSold():
    part_sold_group = PartSoldGroup(
        part_recipient = getRandomReference(PartRecipientGroup),
        customer_part_number_sap = fake.ean(length=13)
    )
    part_sold_group.save()

    start_date = fake.date_time()
    end_date = fake.date_time_between(start_date=start_date, end_date="+10y")
    part_sold = PartSold(
        sap_number = getRandomReference(SapNumber),
        part_sold_group = part_sold_group,
        customer_part_number = fake.ean(length=13),
        customer_group = getRandomReference(CustomerGroup),
        contract_group = getRandomReference(PartSoldContractGroup),
        currency = getRandomReference(Currency),
        description = random.choice([fake.text(), None]),
        validity_start_date = random.choice([start_date, None]),
        validity_end_date = random.choice([end_date, None]),
        cbd_date = fake.date_time(),
        creator = getRandomUser(),
        date = getRandomDateTime()
    )
    part_sold.save()

    for _ in range(random.randint(1, 5)):
        part_sold_price_component = PartSoldPriceComponent(
            part_sold = part_sold,
            value = random.uniform(0, 100),
            saveable = random.choice([True, False]),
            part_sold_price_component_type = getRandomReference(PartSoldPriceComponentType),
            validity_start_date = random.choice([start_date, None]),
            validity_end_date = random.choice([end_date, None])
        )
        part_sold_price_component.save()
    
    for _ in range(random.randint(1, 5)):
        part_sold_material_price_component = PartSoldMaterialPriceComponent(
            part_sold = part_sold,
            part_sold_material_price_type = getRandomReference(PartSoldMaterialPriceType),
            basis = random.uniform(0, 100),
            variable = random.choice([True, False]),
            use_gross_weight = random.choice([True, False]),
            current_saveable = random.choice([True, False]),
            basis_saveable = random.choice([True, False]),
            validity_start_date = random.choice([start_date, None]),
            validity_end_date = random.choice([end_date, None])
        )
        part_sold_material_price_component.save()

    for mat_type in MaterialType.objects.all():
        skip = random.choice([True, *[False]*4])
        if skip:
            continue
        part_sold_material_weight = PartSoldMaterialWeight(
            part_sold = part_sold,
            part_sold_material_type = mat_type,
            gross_weight = random.uniform(0, 100),
            net_weight = random.uniform(0, 100)
        )
        part_sold_material_weight.save()

    for _ in range(random.randint(1, 5)):
        part_sold_saving = PartSoldSaving(
            part_sold = part_sold,
            saving_date = fake.date_time(),
            saving_rate = random.uniform(0, 100),
            saving_unit = getRandomReference(SavingUnit)
        )
        part_sold_saving.save()

    deactivateLastObjectRandomly(part_sold)