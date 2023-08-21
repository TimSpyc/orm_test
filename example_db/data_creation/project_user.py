if __name__ == '__main__':
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'orm_test.settings')

    import django
    django.setup()

from faker import Faker
import random
from auxiliary import getRandomReference, deactivateLastObjectRandomly, getRandomUser, getRandomDateTime
from backend.models import (
    ProjectUserGroup,
    ProjectUser,
    ProjectGroup,
    User,
    ProjectUserRole,
)

fake = Faker()

def populateProjectUser():
    project_user_group = ProjectUserGroup(
        user = getRandomReference(User),
        project_group = getRandomReference(ProjectGroup)
    )
    project_user_group.save()

    project_user = ProjectUser(
        project_user_group = project_user_group,
        creator = getRandomUser(),
        date = getRandomDateTime()
    )

    project_user.save()
    for _ in range(random.randint(0,5)):
        project_user.project_user_role.add(getRandomReference(ProjectUserRole))

    deactivateLastObjectRandomly(project_user)
