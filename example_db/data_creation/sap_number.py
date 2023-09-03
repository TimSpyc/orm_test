if __name__ == '__main__':
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'orm_test.settings')

    import django
    django.setup()

from faker import Faker
import random
from auxiliary import getRandomDateTime, getRandomUser, deactivateLastObjectRandomly, getUniqueNumber
from backend.models import SapNumber, SapNumberGroup

fake = Faker()

def populateSapNumber():
    sap_number_group = SapNumberGroup(
        sap_number = getUniqueNumber(
            SapNumberGroup,
            'sap_number',
            lambda: f'{random.randint(6000000, 7000000):07}'
        ),
    )
    sap_number_group.save()

    sap_number = SapNumber.objects.create(
        sap_number_group = sap_number_group,
        description = fake.text(max_nb_chars=255),
        alu_net_weight = random.uniform(0.5, 75.5),
        creator = getRandomUser(),
        date = getRandomDateTime()
    )
    sap_number.save()
    deactivateLastObjectRandomly(sap_number)
