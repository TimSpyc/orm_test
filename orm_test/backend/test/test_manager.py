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

from django.test import TestCase
from backend.models import User, ProjectUserRole
from manager.project_manager import ProjectManager
from manager.project_user_manager import ProjectUserManager

class ProjectManagerTests(TestCase):
    def setUp(self):
        self.creator_user = User.objects.create(username="creator_user", email="creator@example.com")
        self.project_manager = ProjectManager.create(1, "Test Project", self.creator_user.id)

    def test_project_manager_create(self):
        self.assertIsNotNone(self.project_manager)
        self.assertEqual(self.project_manager.name, "Test Project")
        self.assertEqual(self.project_manager.number, 1)

    def test_project_manager_update(self):
        self.project_manager.update(2, "Updated Test Project", self.creator_user.id)
        self.assertEqual(self.project_manager.name, "Updated Test Project")
        self.assertEqual(self.project_manager.number, 2)

    def test_project_manager_deactivate(self):
        self.project_manager.deactivate()
        self.assertFalse(self.project_manager.active)

class ProjectUserManagerTests(TestCase):
    def setUp(self):
        self.creator_user = User.objects.create(username="creator_user", email="creator@example.com")
        self.project_manager = ProjectManager.create(1, "Test Project", self.creator_user.id)

        self.project_user_role1 = ProjectUserRole.objects.create(role_name="Role1")
        self.project_user_role2 = ProjectUserRole.objects.create(role_name="Role2")

        self.project_user_manager = ProjectUserManager.create(
            self.project_manager.group_id,
            self.creator_user.id,
            self.creator_user.id,
            [self.project_user_role1.id, self.project_user_role2.id]
        )

    def test_project_user_manager_create(self):
        self.assertIsNotNone(self.project_user_manager)
        self.assertEqual(self.project_user_manager.user.username, "creator_user")
        self.assertEqual(len(self.project_user_manager.roles), 2)

    def test_project_user_manager_update(self):
        new_user = User.objects.create(username="new_user", email="new@example.com")
        self.project_user_manager.update(new_user.id, self.creator_user.id, [self.project_user_role1.id])
        self.assertEqual(self.project_user_manager.user.username, "new_user")
        self.assertEqual(len(self.project_user_manager.roles), 1)

    def test_project_user_manager_deactivate(self):
        self.project_user_manager.deactivate()
        self.assertFalse(self.project_user_manager.active)