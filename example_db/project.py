if __name__ == '__main__':
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'orm_test.settings')

    import django
    django.setup()

from faker import Faker
import random
from auxiliary import getRandomDateTime, modelCreationDict, getRandomUser, deactivateLastObjectRandom
from backend.models import ProjectGroup, Project

fake = Faker()

def createFakeProjectWithHistory():
    proj_group = ProjectGroup()
    proj_group.save()

    for _ in range(random.randint(1, 9)):
        proj_dict = {
            "name": fake.bs(),
            "project_number": random.choice([
                f'AP{random.randint(10000, 99999)}',
                f'CST-{random.randint(100, 999)}',
                None
            ]),
            "project_group": proj_group,
            "creator": getRandomUser(),
            "date": getRandomDateTime()
        }

        proj = Project(**modelCreationDict(proj_dict, Project, proj_group))
        proj.save()
    deactivateLastObjectRandom(proj)