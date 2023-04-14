from django.test import TestCase
from backend.src.auxiliary.manager import GeneralManager

from backend.models import GroupTable, DataTable, ReferenceTable
from django.db import models

class TestProjectGroup(models.Model):
    """
    A Django model representing a TestProject group.
    """
    def __str__(self):
        return f'{self.id}'

    class Meta:
        app_label = 'backend'

class TestProject(models.Model):
    """
    A Django model representing a TestProject, including its name, TestProject number, and associated TestProject group.
    """
    name = models.CharField(max_length=255)
    project_number = models.CharField(max_length=255, unique=False)
    project_group = models.ForeignKey(TestProjectGroup, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'backend'

class TestProjectUserGroup(models.Model):
    """
    A Django model representing a TestProject user group, which associates a user with a TestProject group.
    """
    def __str__(self):
        return f'{self.id}'

    class Meta:
        app_label = 'backend'


class TestProjectUserRole(models.Model):
    """
    A Django model representing a TestProject user role, which includes a role name.
    """
    role_name = models.CharField(max_length=255)

    def __str__(self):
        return self.role_name

    class Meta:
        app_label = 'backend'


class TestProjectUser(models.Model):
    """
    A Django model representing a TestProject user, including their TestProject user group and TestProject user roles.
    """
    project_user_group = models.ForeignKey(TestProjectUserGroup, on_delete=models.CASCADE)
    project_user_role = models.ManyToManyField(TestProjectUserRole, blank=False)

    def __str__(self):
        return f'TestProjectUser {self.id}'

    class Meta:
        app_label = 'backend'


class TestSearchForColumn(TestCase):
    def setUp(self):
        self.column_list = ['name', 'description', 'start_date', 'end_date', 'owner_id', 'owner', 'member_id_list', 'member']

    def test_search_for_column(self):
        result = GeneralManager._GeneralManager__searchForColumn('owner_id', self.column_list)
        #result = (db_column_exists, column_name, is_reverencing_model, is_many_to_many)
        self.assertEqual(result, (True, 'owner', True, False))

        result = GeneralManager._GeneralManager__searchForColumn('member_id_list', self.column_list)
        self.assertEqual(result, (True, 'member', False, True))

        result = GeneralManager._GeneralManager__searchForColumn('nonexistent_column', self.column_list)
        self.assertEqual(result, (False, 'nonexistent_column', False, False))

class TestCheckIfColumnReferencesManyToMany(TestCase):
    def setUp(self):
        self.column_list = ['name', 'description', 'start_date', 'end_date', 'owner_id', 'owner', 'member_id_list', 'member']

    def test_check_if_column_references_many_to_many(self):
        result = GeneralManager._GeneralManager__checkIfColumnReferencesManyToMany('member_id_list', self.column_list)
        self.assertEqual(result, ('member', True))

        result = GeneralManager._GeneralManager__checkIfColumnReferencesManyToMany('owner_id', self.column_list)
        self.assertEqual(result, ('owner_id', False))

        result = GeneralManager._GeneralManager__checkIfColumnReferencesManyToMany('nonexistent_column', self.column_list)
        self.assertEqual(result, ('nonexistent_column', False))

class TestCheckIfColumnReferencesModel(TestCase):
    def setUp(self):
        self.column_list = ['name', 'description', 'start_date', 'end_date', 'owner_id', 'owner', 'member_id_list', 'member']

    def test_check_if_column_references_model(self):
        result = GeneralManager._GeneralManager__checkIfColumnReferencesModel('owner_id', self.column_list)
        self.assertEqual(result, ('owner', True))

        result = GeneralManager._GeneralManager__checkIfColumnReferencesModel('member_id_list', self.column_list)
        self.assertEqual(result, ('member_id_list', False))

        result = GeneralManager._GeneralManager__checkIfColumnReferencesModel('nonexistent_column', self.column_list)
        self.assertEqual(result, ('nonexistent_column', False))

class TestGetValueForReferencedModelById(TestCase):
    @classmethod
    def setUpTestData(cls):
        project_group = TestProjectGroup.objects.create()
        TestProject.objects.create(
            name='Test TestProject',
            project_number='123456',
            project_group=project_group
        )

    def test_get_value_for_referenced_model_by_id(self):
        current_model = TestProject
        db_column = 'project_group'
        id = 1
        result = GeneralManager._GeneralManager__getValueForReverencedModelById(current_model, db_column, id)
        self.assertEqual(result, TestProjectGroup.objects.get(id=id))

class TestGetValueForManyToManyByIdList(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Erstellen Sie Beispielprojektbenutzergruppen, -rollen und -benutzer
        project_user_group = TestProjectUserGroup.objects.create()

        project_user_role1 = TestProjectUserRole.objects.create(role_name='Role 1')
        project_user_role2 = TestProjectUserRole.objects.create(role_name='Role 2')

        project_user = TestProjectUser.objects.create(project_user_group=project_user_group)
        project_user.project_user_role.add(project_user_role1)
        project_user.project_user_role.add(project_user_role2)

    def test_get_value_for_many_to_many_by_id_list(self):
        current_model = TestProjectUser
        db_column = 'project_user_role'
        id_list = [1, 2]
        result = GeneralManager._GeneralManager__getValueForManyToManyByIdList(current_model, db_column, id_list)
        expected_result = TestProjectUserRole.objects.filter(id__in=id_list)
        self.assertQuerysetEqual(result, expected_result, transform=lambda x: x, ordered=False)

class TestGetValueAndColumnIfExists(TestCase):
    @classmethod
    def setUpTestData(cls):
        project_group = TestProjectGroup.objects.create()
        TestProject.objects.create(
            name='Test TestProject',
            project_number='123456',
            project_group=project_group
        )

    def test_get_value_and_column_if_exists(self):
        model = TestProject
        column_list = ['name', 'project_number', 'project_group_id', 'related_project_groups']
        db_column = 'project_group_id'
        value = 1
        result = GeneralManager._GeneralManager__getValueAndColumnIfExists(db_column, column_list, model, value)
        # result = (is_in_model, db_column, value)
        self.assertEqual(result, (True, 'project_group_id', TestProjectGroup.objects.get(id=value).id))