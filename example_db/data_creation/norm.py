if __name__ == '__main__':
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'orm_test.settings')

    import django
    django.setup()

from faker import Faker
from auxiliary import getRandomReference, deactivateLastObjectRandomly
from backend.models import Norm, NormGroup, NormType

fake = Faker()

def populateNorm():
    norm_group = NormGroup()
    norm_group.save()

    norm = Norm.objects.create(
        norm_group = norm_group,
        description = fake.text(max_nb_chars=255),
        norm_type = getRandomReference(NormType)
    )
    
    deactivateLastObjectRandomly(norm)
