from django.test import TestCase
from backend.src.auxiliary.manager import GeneralManager
from datetime import datetime
from .models_for_testing import TestProjectGroup, TestProject, TestProjectUserGroup, TestProjectUserRole, TestProjectUser
from backend.models import User
from django.core.exceptions import FieldDoesNotExist


class TestSearchForColumn(TestCase):
    def setUp(self):
        self.column_list = ['name', 'description', 'start_date', 'end_date', 'owner_id', 'owner', 'member_id_list', 'member']

    def test_column_references_model(self):
        result = GeneralManager._GeneralManager__searchForColumn('owner_id', self.column_list)
        #result = (db_column_exists, column_name, is_reverencing_model, is_many_to_many)
        self.assertEqual(result, (True, 'owner', True, False))

    def test_column_does_not_reference_model(self):
        result = GeneralManager._GeneralManager__searchForColumn('member_id_list', self.column_list)
        self.assertEqual(result, (True, 'member', False, True))

    def test_column_references_non_existent_model(self):
        result = GeneralManager._GeneralManager__searchForColumn('nonexistent_column', self.column_list)
        self.assertEqual(result, (False, 'nonexistent_column', False, False))

class TestCheckIfColumnReferencesManyToMany(TestCase):
    def setUp(self):
        self.column_list = ['name', 'description', 'start_date', 'end_date', 'owner_id', 'owner', 'member_id_list', 'member']

    def test_column_references_many_to_many(self):
        result = GeneralManager._GeneralManager__checkIfColumnReferencesManyToMany('member_id_list', self.column_list)
        self.assertEqual(result, ('member', True))
    
    def test_column_does_not_reference_many_to_many(self):
        result = GeneralManager._GeneralManager__checkIfColumnReferencesManyToMany('owner_id', self.column_list)
        self.assertEqual(result, ('owner_id', False))
    
    def test_column_references_non_existent_many_to_many(self):
        result = GeneralManager._GeneralManager__checkIfColumnReferencesManyToMany('nonexistent_column', self.column_list)
        self.assertEqual(result, ('nonexistent_column', False))

class TestCheckIfColumnReferencesModel(TestCase):
    def setUp(self):
        self.column_list = ['name', 'description', 'start_date', 'end_date', 'owner_id', 'owner', 'member_id_list', 'member']

    def test_get_existing_referenced_model_by_id(self):
        result = GeneralManager._GeneralManager__checkIfColumnReferencesModel('owner_id', self.column_list)
        self.assertEqual(result, ('owner', True))
    
    def test_get_non_existent_referenced_model_by_id(self):
        result = GeneralManager._GeneralManager__checkIfColumnReferencesModel('member_id_list', self.column_list)
        self.assertEqual(result, ('member_id_list', False))
    
    def test_invalid_model_column(self):
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
        project_user_group = TestProjectUserGroup.objects.create()

        project_user_role1 = TestProjectUserRole.objects.create(role_name='Role 1')
        project_user_role2 = TestProjectUserRole.objects.create(role_name='Role 2')

        project_user = TestProjectUser.objects.create(project_user_group=project_user_group)
        project_user.project_user_role.add(project_user_role1)
        project_user.project_user_role.add(project_user_role2)

    def test_get_existing_many_to_many_by_id_list(self):
        current_model = TestProjectUser
        db_column = 'project_user_role'
        id_list = [1, 2]
        result = GeneralManager._GeneralManager__getValueForManyToManyByIdList(current_model, db_column, id_list)
        expected_result = TestProjectUserRole.objects.filter(id__in=id_list)
        self.assertQuerysetEqual(result, expected_result, transform=lambda x: x, ordered=False)

    def test_get_non_existent_many_to_many_by_id_list(self):
        value = GeneralManager._GeneralManager__getValueForManyToManyByIdList(TestProjectUser, "project_user_role", [999, 1000])
        self.assertIsNotNone(value)
        self.assertEqual(len(value), 0)

    def test_invalid_model_column(self):
        with self.assertRaises(FieldDoesNotExist):
            value = GeneralManager._GeneralManager__getValueForManyToManyByIdList(TestProjectUser, "non_existent_column", [1, 2])


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

    def test_column_exists_in_model(self):
        column_list = ['name', 'project_number', 'project_group_id', 'related_project_groups']
        result = GeneralManager._GeneralManager__getValueAndColumnIfExists("name", column_list, TestProject, "example_value")
        self.assertEqual(result, (True, "name", "example_value"))

    def test_column_does_not_exist_in_model(self):
        column_list = ['name', 'project_number', 'project_group_id', 'related_project_groups']
        result = GeneralManager._GeneralManager__getValueAndColumnIfExists("non_existent_column", column_list, TestProject, "example_value")
        self.assertEqual(result, (False, "non_existent_column", "example_value"))