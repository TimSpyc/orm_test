if __name__ == '__main__':
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'orm_test.settings')

    import django
    django.setup()

from faker import Faker
import random
from auxiliary import getRandomReference
from backend.models import Material, MaterialGroup, NormGroup, MaterialType, MaterialAlloyGroup, MaterialAlloyTreatmentGroup

fake = Faker()

def populateMaterial():
    material_group = MaterialGroup()
    material_group.save()

    material= Material(
        material_group = material_group,
        material_type = getRandomReference(MaterialType),
        material_alloy = getRandomReference(MaterialAlloyGroup),
        material_alloy_treatment = getRandomReference(MaterialAlloyTreatmentGroup),
        remark = fake.text(),
    )
    material.save()
    for _ in range(random.randint(0,5)):
        material.add(customer_norm = getRandomReference(NormGroup))
    
    material.save()
