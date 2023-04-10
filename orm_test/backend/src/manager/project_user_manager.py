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

from backend.models import ProjectUserGroup, ProjectUser, User, ProjectUserRole
from exceptions import NonExistentGroupError
from datetime import datetime
from manager import GeneralManager


class ProjectUserManager(GeneralManager):
    def __init__(self, project_user_group_id, date=None, use_cache=True):

        project_user_group, project_user = super().__init__(
            group_id=project_user_group_id,
            group_model=ProjectUserGroup,
            data_model=ProjectUser,
            date=date,
            use_cache=use_cache
        )

        self.project_group_id = project_user_group.project_group_id
        self.user_id = project_user_group.user_id
        self.user = project_user_group.user
        self.roles = [{"id": role.id, "name": role.role_name}
                      for role in project_user.project_user_roles.all()]
        self._project_manager = None

    @property
    def project_manager(self):
        from project_manager import ProjectManager
        if self._project_manager is None:
            self._project_manager = ProjectManager(self.project_group_id, self.date)
        return self._project_manager

    @classmethod
    def create(cls, project_group_id, creator_user_id, creator_creator_user_id, project_user_role_ids):
        project_user_group, created = ProjectUserGroup.objects.get_or_create(
            project_group_id=project_group_id,
            user=User.objects.get(id=creator_user_id)
        )

        new_project_user = ProjectUser(
            date=datetime.now(),
            project_user_group=project_user_group,
            creator=User.objects.get(id=creator_creator_user_id),
            active=True
        )
        new_project_user.save()

        for role_id in project_user_role_ids:
            role = ProjectUserRole.objects.get(id=role_id)
            new_project_user.project_user_roles.add(role)

        new_project_user.save()

        project_user_manager = cls(project_user_group.id)
        project_user_manager.updateCache()
        
        return project_user_manager

    def deactivate(self):
        project_user = ProjectUser.objects.get(id=self.id)
        project_user.active = False
        project_user.save()

        new_project_user = ProjectUser(
            date=datetime.now(),
            project_user_group_id=self.group_id,
            creator=self.creator_creator_user_id,
            active=False
        )
        new_project_user.save()

        for role in self.roles:
            role_obj = ProjectUserRole.objects.get(id=role["id"])
            new_project_user.project_user_roles.add(role_obj)

        new_project_user.save()
        self.active = False
        self.updateCache()

    def update(self, new_creator_user_id, creator_creator_user_id, project_user_role_ids):
        project_user_group = ProjectUserGroup.objects.get(id=self.group_id)

        new_project_user = ProjectUser(
            project_user_group=project_user_group,
            user=User.objects.get(id=new_creator_user_id),
            date=datetime.now(),
            creator=User.objects.get(id=creator_creator_user_id),
            active=True
        )
        new_project_user.save()

        for role_id in project_user_role_ids:
            new_project_user.project_user_roles.add(
                ProjectUserRole.objects.get(id=role_id))

        new_project_user.save()

        self.id = new_project_user.id
        self.date = new_project_user.date
        self.creator_creator_user_id = new_project_user.creator_user.id
        self.roles = [{"id": role.id, "name": role.role_name}
                      for role in new_project_user.project_user_roles.all()]
        self.active = new_project_user.active
        self.updateCache()