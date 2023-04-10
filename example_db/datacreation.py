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

from datetime import datetime

# Importiere Modelle und Manager-Klassen
from backend.src.manager.project_manager import ProjectManager
from backend.src.manager.project_user_manager import ProjectUserManager
from backend.models import User, ProjectUserRole
import db

db.truncate_all_tables()

# Erstelle Beispieldaten für die User-Tabelle
users_data = [
    {'name': 'Alice', 'microsoft_id': 'A'},
    {'name': 'Bob', 'microsoft_id': 'B'},
    {'name': 'Charlie', 'microsoft_id': 'C'}
]

# Erstelle Beispieldaten für die ProjectUserRole-Tabelle
roles_data = [
    {'role_name': 'Admin'},
    {'role_name': 'Developer'},
    {'role_name': 'Viewer'}
]

# Füge die Benutzer und Rollen zur Datenbank hinzu
for user_data in users_data:
    user = User(**user_data)
    user.save()

for role_data in roles_data:
    role = ProjectUserRole(**role_data)
    role.save()

# Erstelle ein Projekt mit dem ProjectManager
project_manager = ProjectManager.create(1, 'Testprojekt 1', 1)

# Erstelle einen ProjectUser mit dem ProjectUserManager
project_user_manager = ProjectUserManager.create(project_manager.group_id, 1, 1, [1])

# Erstelle weitere Projekte und ProjectUser
project_manager_2 = ProjectManager.create(2, 'Testprojekt 2', 2)
project_user_manager_2 = ProjectUserManager.create(project_manager_2.group_id, 2, 2, [1, 2])

project_manager_3 = ProjectManager.create(3, 'Testprojekt 3', 3)
project_user_manager_3 = ProjectUserManager.create(project_manager_3.group_id, 3, 3, [3])
