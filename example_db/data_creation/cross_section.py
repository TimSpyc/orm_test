if __name__ == '__main__':
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'orm_test.settings')

    import django
    django.setup()

from faker import Faker
import random
from auxiliary import drawingNumberGenerator, getRandomReference, deactivateLastObjectRandomly
from backend.models import CrossSectionGroup, CrossSection, NormGroup

fake = Faker()

def populateCrossSection():

    cross_section_group = CrossSectionGroup(
        drawing_number = drawingNumberGenerator('Q'),
        drawing_revision = random.randint(0, 100)
    )
    cross_section_group.save()

    cross_section = CrossSection(
        cross_section_group = cross_section_group,
        cross_section_tolerance_norm = getRandomReference(NormGroup),
        customer_tolerance = fake.text(max_nb_chars=255),
        extrusion_plant_tooling_number = fake.text(max_nb_chars=255),
    )
    cross_section.save()

    deactivateLastObjectRandomly(cross_section)