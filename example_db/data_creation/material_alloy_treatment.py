if __name__ == '__main__':
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'orm_test.settings')

    import django
    django.setup()

from faker import Faker
import random
from backend.models import MaterialAlloyTreatment, MaterialAlloyTreatmentGroup
from auxiliary import deactivateLastObjectRandomly, getRandomUser, getRandomDateTime

fake = Faker()

def populateMaterialAlloyTreatment():
    material_alloy_treatment_group = MaterialAlloyTreatmentGroup(
        temperature = random.randint(100, 300),
        duration = random.randint(45, 1800),
    )
    material_alloy_treatment_group.save()

    material_alloy_treatment = MaterialAlloyTreatment(
        remark = random.choice([fake.text(max_nb_chars=200), None]),
        material_alloy_treatment_group = material_alloy_treatment_group,
        creator = getRandomUser(),
        date = getRandomDateTime()
    )
    material_alloy_treatment.save()

    deactivateLastObjectRandomly(material_alloy_treatment)
    