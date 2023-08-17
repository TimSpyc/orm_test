if __name__ == '__main__':
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'orm_test.settings')

    import django
    django.setup()

from faker import Faker
import random
from auxiliary import deactivateLastObjectRandomly, getRandomUser, getRandomDateTime
from backend.models import PartRecipient, PartRecipientGroup

fake = Faker()

def populatePartRecipient():
    part_recipient_group = PartRecipientGroup(
        number = f'{random.randint(1, 1000000):07}'
    )
    part_recipient = PartRecipient.objects.create(
        part_recipient_group = part_recipient_group,
        description = fake.name(),
        creator = getRandomUser(),
        date = getRandomDateTime()
    )
    part_recipient.save()
    deactivateLastObjectRandomly(part_recipient)
