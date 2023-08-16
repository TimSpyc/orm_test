if __name__ == '__main__':
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'orm_test.settings')

    import django
    django.setup()

from faker import Faker
import random
from auxiliary import getRandomReference, deactivateLastObjectRandomly
from backend.models import MaterialAlloy, MaterialAlloyGroup, NormGroup

fake = Faker()

def populateMaterialAlloy():
    material_alloy_group = MaterialAlloyGroup()
    material_alloy_group.save()

    material_alloy= MaterialAlloy(
        material_alloy_group = material_alloy_group,
        norm = getRandomReference(NormGroup),
        chemical_symbol = fake.word(),
        internal_name = fake.word(),
        density = random.choice(2.7, 2.7, 2.7, 7.85, 8.9),
    )
    material_alloy.save()

    deactivateLastObjectRandomly(material_alloy)