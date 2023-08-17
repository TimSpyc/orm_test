if __name__ == '__main__':
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'orm_test.settings')

    import django
    django.setup()

from faker import Faker
import random
from auxiliary import getRandomReference, deactivateLastObjectRandomly, getRandomUser, getRandomDateTime
from backend.models import (
    ProjectStaffCost,
    ProjectStaffCostGroup,
    ProjectGroup,
    User,
    ProjectStaffCostTask
)

fake = Faker()

def populateProjectStaffCost():
    project_staff_cost_group = ProjectStaffCostGroup(
        project_group = getRandomReference(ProjectGroup),
        user = getRandomReference(User),
        project_staff_cost_task = getRandomReference(ProjectStaffCostTask),
        work_date = fake.date_between(start_date='-1y', end_date='today')
    )

    project_staff_cost_group.save()

    project_staff_cost = ProjectStaffCost(
        project_staff_cost_group = project_staff_cost_group,
        hours = random.uniform(0, 10),
        creator = getRandomUser(),
        date = getRandomDateTime()
    )
    project_staff_cost.save()

    deactivateLastObjectRandomly(project_staff_cost)
