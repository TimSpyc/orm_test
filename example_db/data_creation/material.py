if __name__ == '__main__':
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'orm_test.settings')

    import django
    django.setup()

from faker import Faker
import random
from auxiliary import getRandomReference, deactivateLastObjectRandomly, getRandomUser, getRandomDateTime
from backend.models import Material, MaterialGroup, NormGroup, MaterialType, MaterialAlloyGroup, MaterialAlloyTreatmentGroup

fake = Faker()

def populateMaterial():
    material_group = MaterialGroup()
    material_group.save()

    material= Material(
        material_group = material_group,
        material_type = getRandomReference(MaterialType),
        material_alloy = getRandomReference(MaterialAlloyGroup),
        remark = fake.text(),
        creator = getRandomUser(),
        date = getRandomDateTime()
    )
    material.save()
    for _ in range(random.randint(0,5)):
        material.customer_norm.add(getRandomReference(NormGroup))

    for _ in range(random.randint(0,5)):
        material.material_alloy_treatment.add(
            getRandomReference(MaterialAlloyTreatmentGroup)
        )

    material.save()
    deactivateLastObjectRandomly(material)