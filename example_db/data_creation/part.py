if __name__ == '__main__':
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'orm_test.settings')

    import django
    django.setup()

from faker import Faker
import random
from auxiliary import getRandomReference, drawingNumberGenerator, deactivateLastObjectRandomly
from backend.models import (
    Part,
    PartGroup,
    PartType,
    CrossSectionGroup,
    SemiFinishedProductType,
    MaterialGroup,
    NormGroup
)

fake = Faker()

def populatePart():
    part_group = PartGroup(
        drawing_number = random.choice(drawingNumberGenerator('E'), drawingNumberGenerator('Z')),
        drawing_revision = random.randint(1, 100)
    )
    part_group.save()

    weight = random.uniform(0, 100)
    length = random.uniform(10, 6000)
    linear_weight = weight / length *1000

    part = Part(
        part_group = part_group,
        name = fake.name(),
        part_type = getRandomReference(PartType),
        cross_section_group = getRandomReference(CrossSectionGroup),
        drawing_date = fake.date_time(),
        customer_drawing_number = fake.ean(length=13),
        customer_drawing_revision = fake.ean(length=13),
        customer_part_number = fake.ean(length=13),
        customer_part_revision = fake.ean(length=13),
        surface_treatment = fake.name(),
        customer_surface_treatment = fake.name(),
        weight = weight,
        linear_weight = linear_weight,
        length = length,
        tolerance = fake.name(),
        customer_tolerance = fake.name(),
        semi_finished_product_type = getRandomReference(SemiFinishedProductType),
        material_group = getRandomReference(MaterialGroup),
        delivery_temper = fake.name(),
        material_norm_customer = getRandomReference(NormGroup)
    )
    part.save()

    deactivateLastObjectRandomly(part)