if __name__ == '__main__':
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'orm_test.settings')

    import django
    django.setup()

from faker import Faker
from auxiliary import getRandomReference, deactivateLastObjectRandomly, getRandomUser, getRandomDateTime
from backend.models import (
    File,
    FileGroup,
    FileType
)

fake = Faker()

def populateFile():
    file_group = FileGroup()
    file_group.save()

    file = File(
        file_group = file_group,
        name = fake.name(),
        file_type = getRandomReference(FileType),
        creator = getRandomUser(),
        date= getRandomDateTime(),
    )
    file.save()

    deactivateLastObjectRandomly(file)