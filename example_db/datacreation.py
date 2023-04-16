if __name__ == '__main__':
    import sys
    import os

    sys.path.append(r'C:\Users\Spyc\Django_ORM')
    sys.path.append(r'C:\Users\Spyc\Django_ORM\orm_test')
    sys.path.append(r'C:\Users\Spyc\Django_ORM\orm_test\orm_test')
    sys.path.append(r'C:\Users\Spyc\Django_ORM\orm_test\backend\src\manager')
    sys.path.append(r'C:\Users\Spyc\Django_ORM\orm_test\backend\src\auxiliary')
    sys.path.append(r'C:\Users\Spyc\Django_ORM\orm_test\backend')
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'orm_test.settings')

    import django
    django.setup()

import random
from datetime import datetime, timedelta
from backend.models import (
    User,
    ProjectGroup,
    Project,
    ProjectUserGroup,
    ProjectUserRole,
    ProjectUser,
    DerivativeConstelliumGroup,
    DerivativeType,
    PredictionAccuracy,
    DerivativeConstellium,
)
import db

db.truncate_all_tables()
# Users
user_list = []
for i in range(5):
    user = User.objects.create(
        microsoft_id=f"user{i}",
        name=f"Name{i}",
        last_name=f"LastName{i}",
        email=f"user{i}@example.com",
        last_login=datetime.now() - timedelta(days=random.randint(1, 30), minutes=random.randint(1, 30), seconds=random.randint(1, 60)) - timedelta(days=random.randint(1, 30), minutes=random.randint(1, 30), seconds=random.randint(1, 60)),
    )
    user_list.append(user)

# Project Groups
project_group_list = []
for i in range(3):
    project_group = ProjectGroup.objects.create()
    project_group_list.append(project_group)

# Projects
project_list = []
for i, project_group in enumerate(project_group_list):
    for j in range(3):
        project = Project.objects.create(
            name=f"Project {i}-{j}",
            project_number=f"P{i}-{j}",
            project_group=project_group,
            date=datetime.now() - timedelta(days=random.randint(1, 30), minutes=random.randint(1, 30), seconds=random.randint(1, 60)),
            creator=user_list[random.randint(0, len(user_list) - 1)],
        )
        project_list.append(project)

# Project User Groups
project_user_group_list = []
for user in user_list:
    for project_group in project_group_list:
        project_user_group = ProjectUserGroup.objects.create(
            user=user,
            project_group=project_group,
        )
        project_user_group_list.append(project_user_group)

# Project User Roles
project_user_role_list = [
    ProjectUserRole.objects.create(role_name="Admin"),
    ProjectUserRole.objects.create(role_name="User"),
    ProjectUserRole.objects.create(role_name="Guest"),
]

# Project Users
for project_user_group in project_user_group_list:
    project_user = ProjectUser.objects.create(
        project_user_group=project_user_group,
        date=datetime.now() - timedelta(days=random.randint(1, 30), minutes=random.randint(1, 30), seconds=random.randint(1, 60)),
        creator=user_list[random.randint(0, len(user_list) - 1)],
    )
    for _ in range(random.randint(1, len(project_user_role_list))):
        project_user.project_user_role.add(
            project_user_role_list[random.randint(0, len(project_user_role_list) - 1)]
        )

# Derivative Constellium Groups
derivative_constellium_group_list = []
for project_group in project_group_list:
    derivative_constellium_group = DerivativeConstelliumGroup.objects.create(
        project_group=project_group
    )
    derivative_constellium_group_list.append(derivative_constellium_group)

# Derivative Types
derivative_type_list = [
    DerivativeType.objects.create(name="Type A"),
    DerivativeType.objects.create(name="Type B"),
    DerivativeType.objects.create(name="Type C"),
]

# Prediction Accuracies
prediction_accuracy_list = [
    PredictionAccuracy.objects.create(name="High"),
    PredictionAccuracy.objects.create(name="Medium"),
    PredictionAccuracy.objects.create(name="Low"),
]

# Derivative Constelliums
for derivative_constellium_group in derivative_constellium_group_list:
    for i in range(3):
        DerivativeConstellium.objects.create(
            derivative_constellium_group=derivative_constellium_group,
            name=f"Derivative {i}",
            sop_date=datetime.now() + timedelta(days=random.randint(1, 30)),
            eop_date=datetime.now() + timedelta(days=random.randint(31, 60)),
            derivative_type=derivative_type_list[random.randint(0, len(derivative_type_list) - 1)],
            estimated_price=random.uniform(1000, 10000),
            estimated_weight=random.uniform(500, 2000),
            prediction_accuracy=prediction_accuracy_list[random.randint(0, len(prediction_accuracy_list) - 1)],
            date=datetime.now() - timedelta(days=random.randint(1, 30), minutes=random.randint(1, 30), seconds=random.randint(1, 60)),
            creator=user_list[random.randint(0, len(user_list) - 1)],
            active=True,
        )

print("Datenbank mit Beispieldaten erfolgreich gefüllt.")