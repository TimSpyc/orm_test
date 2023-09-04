import logging
from unittest.mock import  Mock, patch
from backend.models.caching_models import CacheManager
from backend.src.auxiliary.exceptions import NonExistentGroupError, NotUpdatableError, NotValidIdError
from backend.test.test_property_managers import newAbc, newAbcGroup, newAbcManager, newKunden, newKundenGroup, newProject, newProjectGroup, newProjectUser, newProjectUserGroup, newProjectUserRoles, newXyz, newXyzGroup, newXyzManager
from django.test import TestCase
from backend.src.auxiliary.manager import GeneralManager
from datetime import date, datetime
from .models_for_testing import TestProject2ExtensionTable, TestProjectGroup2, TestProject3, TestProject2, TestProjectGroup, TestProject, TestProjectGroup3, TestProjectUser2, TestProjectUserGroup, TestProjectUserGroup2, TestProjectUserRole, TestProjectUser
from backend.models import User
from django.core.exceptions import FieldDoesNotExist, FieldError


class TestProjectManager(GeneralManager):
    group_model = TestProjectGroup
    data_model = TestProject
    data_extension_model_list: list = []


        
class TestProjectUserManager(GeneralManager):
    group_model = TestProjectUserGroup
    data_model = TestProjectUser
    data_extension_model_list: list = []



class TestSearchForColumn(TestCase):
    def setUp(self):
        self.column_list = ['name', 'description', 'start_date', 'end_date',  'owner', 'member']

    def test_column_references_model(self):
        result = GeneralManager._GeneralManager__searchForColumn('owner_id', self.column_list)
        self.assertEqual(result, (True, 'owner', True, False))

    def test_column_does_not_reference_model(self):
        result = GeneralManager._GeneralManager__searchForColumn('member_id_list', self.column_list)
        self.assertEqual(result, (True, 'member', False, True))

    def test_column_references_non_existent_model(self):
        result = GeneralManager._GeneralManager__searchForColumn('nonexistent_column', self.column_list)
        self.assertEqual(result, (False, 'nonexistent_column', False, False))

    def test_column_does_not_reference_many_to_many(self):
        result = GeneralManager._GeneralManager__searchForColumn('owner_id', self.column_list)
        self.assertEqual(result,(True, 'owner', True, False))

class TestCheckIfColumnReferenceBaseExists(TestCase):
    def setUp(self):   
        self.column_list = ['name', 'description', 'start_date', 'end_date', 'owner_id', 'owner', 'member_id_list', 'member', 'memberabc123']

    def test_with_existing_column_and_reference(self):                                      
        result = GeneralManager._GeneralManager__checkIfColumnReferenceBaseExists('memberabc123', self.column_list, 'abc123')
        self.assertEqual(result,('member',True))

    def test_with_non_existing_reference(self):                                      
        result = GeneralManager._GeneralManager__checkIfColumnReferenceBaseExists('start_date', self.column_list, 'xyzfagadhaergad')
        self.assertEqual(result,('start_date',False))

    def test_column_ends_with_id_list_but_searches_for_id(self):                                      
        result = GeneralManager._GeneralManager__checkIfColumnReferenceBaseExists('member_id_list', self.column_list, '_id')
        self.assertEqual(result,('member_id_list',False))

    def test_with_non_existing_column(self):                                      
        result = GeneralManager._GeneralManager__checkIfColumnReferenceBaseExists('nonexistent_column', self.column_list, '1231asdae')
        self.assertEqual(result,('nonexistent_column',False))    

    def test_with_non_existing_column_and_existing_search_word(self):                                      
        result = GeneralManager._GeneralManager__checkIfColumnReferenceBaseExists('nonexistent_column_id', self.column_list, '_id')
        self.assertEqual(result,('nonexistent_column_id',False))  

class TestCheckIfColumnReferencesManyToMany(TestCase):
    def setUp(self):
        self.column_list = ['name', 'description', 'start_date', 'end_date', 'owner_id', 'owner', 'member']
        self.column_list_without_given_column_model_name = ['name', 'description', 'start_date', 'end_date', 'owner_id', 'owner', 'member_id_list']

    def test_column_references_many_to_many(self):
        result = GeneralManager._GeneralManager__checkIfColumnReferencesManyToMany('member_id_list', self.column_list)
        self.assertEqual(result, ('member', True))
    
    def test_column_does_not_reference_many_to_many(self):
        result = GeneralManager._GeneralManager__checkIfColumnReferencesManyToMany('owner_id', self.column_list)
        self.assertEqual(result, ('owner_id', False))
    
    def test_column_references_non_existent_many_to_many(self):
        result = GeneralManager._GeneralManager__checkIfColumnReferencesManyToMany('nonexistent_column', self.column_list)
        self.assertEqual(result, ('nonexistent_column', False))

    def test_columnName_not_in_list(self):
        result = GeneralManager._GeneralManager__checkIfColumnReferencesManyToMany('member_id_list', self.column_list_without_given_column_model_name)   
        self.assertEqual(result,('member_id_list', False))
    
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
            test_project_group = project_group
        )

        project_group1 = TestProjectGroup.objects.create()
        TestProject.objects.create(
            name='test testproject',
            project_number='1234567',
            test_project_group = project_group1
        )

    def test_get_value_for_referenced_model_by_id(self):
        current_model = TestProject
        db_column = 'test_project_group'
        id = 1
        result = GeneralManager._GeneralManager__getValueForReverencedModelById(current_model, db_column, id)
        self.assertEqual(result, TestProjectGroup.objects.get(id=id))

    def test_get_no_value_for_referenced_model(self):
        current_model = TestProject   
        db_column = 'test_project_group'
        id = 1
        result = GeneralManager._GeneralManager__getValueForReverencedModelById(current_model, db_column, id)
        self.assertNotEqual(result, TestProjectGroup.objects.get(id=2))

    def test_invalid_model(self):
        with self.assertRaises(NameError):
            value = GeneralManager._GeneralManager__getValueForReverencedModelById(non_existing_model, 'test_project_group', 1)

    def test_invalid_model_column(self):
        with self.assertRaises(FieldDoesNotExist):
            value = GeneralManager._GeneralManager__getValueForReverencedModelById(TestProject, 'non_existent_column', 1)

    def test_invalid_id(self):
        with self.assertRaises(NotValidIdError):
            value = GeneralManager._GeneralManager__getValueForReverencedModelById(TestProject, 'test_project_group', 3)
            
    def test_with_no_given_id(self):
       with self.assertRaises(NotValidIdError):
            value = GeneralManager._GeneralManager__getValueForReverencedModelById(TestProject, 'test_project_group', 3)
        
class TestGetValueForManyToManyByIdList(TestCase):
    @classmethod
    def setUpTestData(cls):
        project_user_group = TestProjectUserGroup.objects.create()

        project_user_role1 = TestProjectUserRole.objects.create(role_name='Role 1')
        project_user_role2 = TestProjectUserRole.objects.create(role_name='Role 2')

        project_user = TestProjectUser.objects.create(test_project_user_group=project_user_group)
        project_user.test_project_user_role.add(project_user_role1)
        project_user.test_project_user_role.add(project_user_role2)

    def test_get_existing_many_to_many_by_id_list(self):
        current_model = TestProjectUser
        db_column = 'test_project_user_role'
        id_list = [1, 2]
        result = GeneralManager._GeneralManager__getValueForManyToManyByIdList(current_model, db_column, id_list)
        expected_result = TestProjectUserRole.objects.filter(id__in=id_list)
        self.assertQuerysetEqual(result, expected_result, transform=lambda x: x, ordered=False)


    def test_invalid_model_column(self):
        with self.assertRaises(FieldDoesNotExist):
            value = GeneralManager._GeneralManager__getValueForManyToManyByIdList(TestProjectUser, "non_existent_column", [1, 2])

    def test_invalid_model(self):
        with self.assertRaises(NameError):
            value = GeneralManager._GeneralManager__getValueForManyToManyByIdList(non_existing_model, 'test_project_user_role', [1,2])

    def test_invalid_id_in_list(self):  
        with self.assertRaises(NotValidIdError):
            value = GeneralManager._GeneralManager__getValueForManyToManyByIdList(TestProjectUser, "test_project_user_role", [1, 2, 3])

    def test_with_no_given_id_list(self):
        result = GeneralManager._GeneralManager__getValueForManyToManyByIdList(TestProject, 'test_project_group', [])
        self.assertEqual(list(result), [])

class TestGetValueAndColumnIfExists(TestCase):
    @classmethod
    def setUpTestData(cls):
        project_group = TestProjectGroup.objects.create()
        TestProject.objects.create(
            name='Test TestProject',
            project_number='123456',
            test_project_group=project_group
        )
        project_group1 = TestProjectGroup.objects.create()
        TestProject.objects.create(
            name='Test TestProject1',
            project_number='1234567',
            test_project_group=project_group
        )

        project_user_group = TestProjectUserGroup.objects.create()
        project_user_group1 = TestProjectUserGroup.objects.create()
        project_user_role1 = TestProjectUserRole.objects.create(role_name = 'admin')
        project_user_role2 = TestProjectUserRole.objects.create(role_name = 'test123')

        project_user1 = TestProjectUser.objects.create(
            test_project_user_group = project_user_group
        )
        project_user1.test_project_user_role.add(project_user_role1, project_user_role2)

        project_user2 = TestProjectUser.objects.create(test_project_user_group = project_user_group1)
        project_user2.test_project_user_role.add(project_user_role1)
        
    def test_get_value_and_column_if_exists(self):
        model = TestProject
        column_list = ['name', 'project_number', 'group_id']
        db_column = 'group_id'
        value = 1
        
        result = GeneralManager._GeneralManager__getValueAndColumnIfExists(db_column, column_list, model, value)
        # result = (is_in_model, db_column, value)
        self.assertEqual(result, (True, 'group_id', TestProjectGroup.objects.get(id=value).id))
        self.assertEqual(result, (True, 'group_id', 1))

    def test_column_exists_in_model(self):
        column_list = ['name', 'project_number', 'group_id']
        result = GeneralManager._GeneralManager__getValueAndColumnIfExists("name", column_list, TestProject, "example_value")
        self.assertEqual(result, (True, "name", "example_value"))

    def test_column_does_not_exist_in_model(self):
        column_list = ['name', 'project_number', 'group_id']
        result = GeneralManager._GeneralManager__getValueAndColumnIfExists("non_existent_column", column_list, TestProject, "example_value")
        self.assertEqual(result, (False, "non_existent_column", "example_value"))

    def test_get_value_and_column_if_exists_with_many_to_many_relation(self):
        column_list = ['test_project_user_group', 'test_project_user_role']
        value = [1, 2]
        is_in_model, db_column, value = GeneralManager._GeneralManager__getValueAndColumnIfExists('test_project_user_role_id_list', column_list, TestProjectUser, value)
        self.assertEqual((is_in_model, db_column, list(value)), (True, 'test_project_user_role', list(TestProjectUserRole.objects.filter(id__in=value))))

class TestGetColumnNameList(TestCase):

    @classmethod
    def setUpTestData(cls):
        project_group = TestProjectGroup.objects.create()
        TestProject.objects.create(
            name='TestProject1',
            project_number='123456',
            test_project_group = project_group
        )
    def test_get_column_list(self):
        result = GeneralManager._GeneralManager__getColumnNameList(TestProject)
        column_list = ['id', 'name', 'project_number', 'test_project_group','date', 'creator', 'active']
        self.assertEqual(result,column_list)      
        
class TestFilter(TestCase):
    
    def setUp(self):
        self.test_project_group = TestProjectGroup.objects.create()
        self.user = User.objects.create()
        self.test_project = TestProject.objects.create(
            name='TestProject1',
            project_number='123456',
            test_project_group = self.test_project_group,
            date = datetime(2023, 5, 15),
            creator = self.user,
            active = True
        )
        self.manager = TestProjectManager(group_id = self.test_project_group.id)
    
    def test_filter_with_search_date(self):
        search_date = date(2023, 5, 16)
        result = self.manager.filter(search_date=search_date)

        expected_result = [
            TestProjectManager(group_id= self.test_project_group.id, search_date= search_date)
        ]
        self.assertEqual(result, expected_result)

        
    def test_filter_with_invalid_filter_condition(self):
        with self.assertRaises(ValueError):
            result = self.manager.filter(invalid_field='invalid_value')


    def test_filter_with_other_filter_condition_than_searchDate(self):
        name = 'TestProject1'
        result = self.manager.filter(name = name)
        expected_result = [
            TestProjectManager(group_id= self.test_project_group.id)
        ]
        self.assertEqual(result, expected_result)


    def test_filter_with_no_found_data_in_table(self):
        result = self.manager.filter(name = 'not_existing_data')
        expected_result = [
        ]
        self.assertEqual(result, expected_result)
            
          
    def test_filter_with_multiple_conditions(self):
        search_date = date(2023, 5, 20)
        name = 'TestProject1'
        project_number = '123456'
        result = self.manager.filter(search_date=search_date, project_number=project_number, name = name)
        expected_result = [
            TestProjectManager(group_id=self.test_project_group.id, search_date = search_date)
        ]
        self.assertEqual(result, expected_result)


    def test_filter_with_many_to_many_relations(self):
        self.test_project_user_group = TestProjectUserGroup.objects.create()
        self.test_project_user_role1 = TestProjectUserRole.objects.create(role_name='Role 1')
        self.test_project_user_role2 = TestProjectUserRole.objects.create(role_name='Role 2')

      
        self.test_project_user1 = TestProjectUser.objects.create(test_project_user_group = self.test_project_user_group, creator = self.user)
        self.test_project_user1.test_project_user_role.add(self.test_project_user_role1)
        self.test_project_user1.test_project_user_role.add(self.test_project_user_role2)

        TestProjectUserManager.use_cache = False
        self.many_to_many_manager = TestProjectUserManager(group_id=self.test_project_user_group.id)

        result = self.many_to_many_manager.filter(test_project_user_role = self.test_project_user_role1)
        expected_result = [
            TestProjectUserManager(group_id= self.test_project_user_group.id)
        ]
        self.assertEqual(result, expected_result)

class TestAll(TestCase):
    def setUp(self):
        self.test_project_group = TestProjectGroup.objects.create()
        self.user = User.objects.create()
        
        self.test_project1 = TestProject.objects.create(
            name='TestProject1',
            project_number='123456',
            test_project_group = self.test_project_group,
            date = datetime(2023, 5, 14),
            creator = self.user,
            active = True
        )
        self.test_project2 = TestProject.objects.create(
            name='TestProject2',
            project_number='123',
            test_project_group = self.test_project_group,
            date = datetime(2023, 5, 15),
            creator = self.user,
            active = True
        )
        self.test_project3 = TestProject.objects.create(
            name='TestProject3',
            project_number='12111',
            test_project_group = self.test_project_group,
            date = datetime(2023, 5, 15),
            creator = self.user,
            active = True
        )
        self.manager = TestProjectManager(group_id = self.test_project_group.id)
    
    def test_all_with_search_date(self):
        search_date = date(2023, 5, 17)
        result = self.manager.all(search_date=search_date)

        expected_result = [
            TestProjectManager(group_id= self.test_project_group.id, search_date= search_date)
        ]
        self.assertEqual(result, expected_result)

    def test_all_without_search_date(self):
        result = self.manager.all()

        expected_result = [
            TestProjectManager(group_id= self.test_project_group.id),
        ]
        self.assertEqual(result, expected_result)    

class TestGetDataForGroupAndDataTableByKwargs(TestCase):
    def setUp(self):
        self.data_model_column_list = ['name', 'project_number','test_project_group']
        self.group_model_column_list = ['id']

        GeneralManager.group_model = TestProjectGroup
        GeneralManager.data_model = TestProject
        self.manager = GeneralManager.__new__(GeneralManager)
        
    def test_get_data_for_group_and_data_table_by_kwargs(self):
        group_data_dict, data_data_dict, data_extension_data_dict = self.manager._GeneralManager__getDataForGroupAndDataTableByKwargs(   
            self.data_model_column_list,
            self.group_model_column_list,
            id = 1,
            name = 'testproject1',
            project_number= '123456'
        )
        self.assertEqual(group_data_dict, {'id': 1})
        self.assertEqual(data_data_dict, {'name': 'testproject1', 'project_number': '123456'})

    def test_not_unique_column_names(self):
        with self.assertRaises(ValueError):
            self.data_model_column_list = ['id', 'name', 'project_number','test_project_group']
            self.group_model_column_list = ['id']
            group_data_dict, data_data_dict = self.manager._GeneralManager__getDataForGroupAndDataTableByKwargs(
                self.data_model_column_list,
                self.group_model_column_list,
                name = 'TestProject1',
                id = 1,
                project_number = '123456'
            )
        
    def test_no_corresponding_column_in_model(self):
        with self.assertRaises(ValueError):
            self.data_model_column_list = [ 'project_number','project_group']
            self.group_model_column_list = ['id']
            group_data_dict, data_data_dict = self.manager._GeneralManager__getDataForGroupAndDataTableByKwargs(
                self.data_model_column_list,
                self.group_model_column_list,
                name = 'TestProject1',
                id = 1,
                project_number = '123456'
            )

class TestGetFilteredManagerList(TestCase):
    def setUp(self):
        GeneralManager.group_model = TestProjectGroup
        GeneralManager.data_model = TestProject
        self.manager = GeneralManager.__new__(GeneralManager)

    def test_get_filtered_manager_list(self):
        project_group1 = TestProjectGroup.objects.create()
        test_project1 = TestProject.objects.create(
                        name='TestProject1',
                        project_number='1234567',
                        test_project_group = project_group1,
                        date=datetime(2023, 5, 13))
        test_project2 = TestProject.objects.create(
                        name='TestProject1',
                        project_number='123456',
                        test_project_group = project_group1,
                        date=datetime(2023, 4, 5))

        data_search_dict = {'name': 'TestProject1', 'project_number': '1234567'} 
        group_search_dict = {'id':1} 
        search_date = datetime(2023, 5, 16)

        result = self.manager._GeneralManager__getFilteredManagerList(data_search_dict, group_search_dict, search_date)
        expected_result = [
            {'group_id': project_group1.id, 'search_date': search_date}
        ]
        self.assertEqual(result, expected_result)

    def test_with_empty_dicts_just_search_date(self):   
        project_group1 = TestProjectGroup.objects.create()
        test_project1 = TestProject.objects.create(
                        name='TestProject1',
                        project_number='123456',
                        test_project_group = project_group1,
                        date=datetime(2022, 5, 15))
        
        test_project2 = TestProject.objects.create(
                        name='TestProject1',
                        project_number='1234567',
                        test_project_group = project_group1,
                        date=datetime(2023, 4, 5))
        data_search_dict = {} 
        group_search_dict = {} 
        search_date = datetime(2023, 5, 16)

        result = self.manager._GeneralManager__getFilteredManagerList(data_search_dict, group_search_dict, search_date)
        expected_result = [
            {'group_id': project_group1.id, 'search_date': search_date}
        ]
        self.assertEqual(result, expected_result)

    def test_with_empty_dicts_and_no_search_date(self):
            project_group1 = TestProjectGroup.objects.create()
            project_group2 = TestProjectGroup.objects.create()
            test_project1 = TestProject.objects.create(
                name='TestProject1',
                project_number='123456',
                test_project_group=project_group1,
                date=datetime(2022, 5, 15)
            )
            test_project2 = TestProject.objects.create(
                name='TestProject1',
                project_number='654321',
                test_project_group=project_group2,
                date=datetime(2023, 4, 5)
            )
            test_project3 = TestProject.objects.create(
            name='TestProject2',
            project_number='789012',
            test_project_group=project_group1,
            date=datetime(2023, 5, 16)
        )
 
            data_search_dict = {}
            group_search_dict = {}
            search_date = None

            result = self.manager._GeneralManager__getFilteredManagerList(data_search_dict, group_search_dict, search_date)
            expected_result = [
                {'group_id': project_group1.id, 'search_date': None},
                {'group_id': project_group2.id, 'search_date': None}
            ]
            self.assertEqual(result, expected_result)

    def test_get_filtered_manager_list_with_no_results(self):
        project_group1 = TestProjectGroup.objects.create()
        test_project1 = TestProject.objects.create(
            name='TestProject1',
            project_number='123456',
            test_project_group=project_group1,
            date=datetime(2022, 5, 15)
        )
        test_project2 = TestProject.objects.create(
            name='TestProject1',
            project_number='1234567',
            test_project_group=project_group1,
            date=datetime(2023, 4, 5)
        )
 
        data_search_dict = {'name': 'TestProject2', 'project_number': '654321'}
        group_search_dict = {'id': 1}
        search_date = datetime(2023, 5, 16)
 
        result = self.manager._GeneralManager__getFilteredManagerList(data_search_dict, group_search_dict, search_date)
        expected_result = []
        self.assertEqual(result, expected_result)

 
    def test_with_not_found_data_in_model_table(self):
        project_group1 = TestProjectGroup.objects.create()
        test_project1 = TestProject.objects.create(
            name='TestProject1',
            project_number='123456',
            test_project_group=project_group1,
            date=datetime(2022, 5, 15)
        )
        data_search_dict = {'name': 'invalid_name'}
        group_search_dict = {'id': 2}
        search_date = datetime(2023, 5, 16)

        result = self.manager._GeneralManager__getFilteredManagerList(data_search_dict, group_search_dict, search_date)
        expected_result = []
        self.assertEqual(result, expected_result)

    def test_with_invalid_search_dict_column(self):
        project_group1 = TestProjectGroup.objects.create()
        test_project1 = TestProject.objects.create(
            name='TestProject1',
            project_number='123456',
            test_project_group=project_group1,
            date=datetime(2022, 5, 15)
        )
        data_search_dict = {'not_existing_column': 'invalid_name'}
        group_search_dict = {'not_existing_column': 1}
        search_date = datetime(2023, 5, 16)

        with self.assertRaises(FieldError):
            self.manager._GeneralManager__getFilteredManagerList(data_search_dict, group_search_dict, search_date)

    def test_with_search_date_equals_latest_date(self):
        project_group1 = TestProjectGroup.objects.create()
        test_project1 = TestProject.objects.create(
            name='TestProject2',
            project_number='123456',
            test_project_group=project_group1,
            date=datetime(2023, 5, 15)
        )
        test_project2 = TestProject.objects.create(
            name='TestProject1',
            project_number='654321',
            test_project_group=project_group1,
            date=datetime(2023, 4, 5)
        )
   
        data_search_dict = {'name': 'TestProject2'}
        group_search_dict = {}
        search_date = datetime(2023, 5, 15)

        result = self.manager._GeneralManager__getFilteredManagerList(data_search_dict, group_search_dict, search_date)
        expected_result = [
            {'group_id': project_group1.id, 'search_date': search_date}
        ]
        self.assertEqual(result, expected_result)  

class TestErrorIfNotUpdatable(TestCase):
    def setUp(self):
        self.manager = GeneralManager.__new__(GeneralManager)
        self.manager.group_model = TestProjectGroup
        self.manager.data_model = TestProject
        
        project_group1 = TestProjectGroup.objects.create()
        self.test_project = TestProject.objects.create(
            name='testproject1',
            project_number='1234567',
            test_project_group = project_group1, 
        )
        self.manager._GeneralManager__group_obj = project_group1
        
      
    def test_error_if_not_updatable_latest_date(self):
        self.manager.id = self.test_project.id
        self.manager._GeneralManager__errorIfNotUpdatable()

    def test_not_latest_date(self):
        project_group1 = TestProjectGroup.objects.create()
        different_model = TestProject.objects.create(
             name='testproject2',
             project_number='1234567',
             test_project_group = project_group1
        )
        self.manager.id = different_model.id

        with self.assertRaises(NotUpdatableError):
             self.manager._GeneralManager__errorIfNotUpdatable()

class TestGetGroupModelName(TestCase):
      def setUp(self):

        self.manager = GeneralManager.__new__(GeneralManager) 
        self.manager.group_model = TestProjectGroup
        self.manager.data_model = TestProject
        
      def test_get_group_model_name(self):
            project_group1 = TestProjectGroup.objects.create()
            test_project1 = TestProject.objects.create(
                         name='TestProject1',
                         project_number='123456',
                         test_project_group = project_group1
                         )
            
            group_model_name = self.manager._GeneralManager__getGroupModelName()

            self.assertEqual(group_model_name,'test_project_group')

class TestGetGroupObject(TestCase):
    def setUp(self):
        GeneralManager.group_model = TestProjectGroup
        GeneralManager.data_model = TestProject
        self.manager = GeneralManager.__new__(GeneralManager)
 
    def test_get_group_object(self):
        self.manager.group_id = 1
        group_obj = TestProjectGroup.objects.create(id=self.manager.group_id)
 
        result = self.manager._GeneralManager__getGroupObject()
        self.assertEqual(result, group_obj)
 
    def test_with_invalid_group_id(self):
        self.manager.group_id = 12
        with self.assertRaises(NonExistentGroupError):
            self.manager._GeneralManager__getGroupObject()

class TestGetDataObject(TestCase):
    def setUp(self):
        self.manager = GeneralManager.__new__(GeneralManager)
        self.group_model = TestProjectGroup
        GeneralManager.data_model= TestProject

        self.group_obj = TestProjectGroup.objects.create(id=1)
        self.manager._GeneralManager__group_model_name = 'test_project_group'
        
        #if no search_date , get latest data_obj
    def test_get_data_object_without_search_date(self):
        data_obj1 = TestProject.objects.create(test_project_group=self.group_obj, date= date(2023,5,22))
        data_obj2 = TestProject.objects.create(test_project_group=self.group_obj, project_number='123', date= date(2023,5,21))

        result = self.manager._GeneralManager__getDataObject(self.group_obj, None)
        self.assertEqual(result, data_obj1)

    def test_get_data_object_with_search_date(self):
        data_obj1 = TestProject.objects.create(test_project_group=self.group_obj, date= date(2023,5,22))
        data_obj2 = TestProject.objects.create(test_project_group=self.group_obj, project_number='123', date= date(2023,5,21))

        search_date = date(2023,5,21)
        result = self.manager._GeneralManager__getDataObject(self.group_obj, search_date)
        self.assertEqual(result, data_obj2)
 
    def test_with_non_existing_data_object(self):
        data_obj1 = TestProject.objects.create(test_project_group=self.group_obj, date= date(2023,5,22))
        non_existing_search_date = date(2023,5,19)
        with self.assertRaises(NonExistentGroupError):
            self.manager._GeneralManager__getDataObject(self.group_obj, non_existing_search_date)
 
    def test_get_latest_data_object_with_search_date(self):
        data_obj1 = TestProject.objects.create(test_project_group=self.group_obj, date= date(2023,5,22))
        data_obj2 = TestProject.objects.create(test_project_group=self.group_obj, project_number='123', date= date(2023,5,21))
        search_date = date(2023,5,25)
        result = self.manager._GeneralManager__getDataObject(self.group_obj, search_date)
        self.assertEqual(result, data_obj1)

class TestIsDataUploadable(TestCase):
    def setUp(self):
        self.manager = GeneralManager.__new__(GeneralManager)
 
    def test_is_data_uploadable(self):
        data_dict = {
            'name': 'testproject1', 
            'project_number': '123456',
            'date': datetime(2023, 5, 22),
            'test_project_group': 1
        }
        contains_all_unique_fields, contains_all_not_null_fields, all_not_null_fields_contain_data = self.manager._GeneralManager__isDataUploadable(data_dict, TestProject)
 
        self.assertTrue(contains_all_unique_fields)
        self.assertTrue(contains_all_not_null_fields)
        self.assertTrue(all_not_null_fields_contain_data)
  
    def test_is_data_uploadable_missing_unique_fields(self):
        data_dict = {
            'name': 'testproject1', 
            'project_number': '123456',
            'date': datetime(2023, 5, 22),
            'test_project_group': 1,
            #'ap_no': 12
        }
        contains_all_unique_fields, contains_all_not_null_fields, all_not_null_fields_contain_data = self.manager._GeneralManager__isDataUploadable(data_dict, TestProject2)
 
        self.assertFalse(contains_all_unique_fields)
        self.assertTrue(contains_all_not_null_fields)
        self.assertTrue(all_not_null_fields_contain_data)
 
    def test_is_data_uploadable_missing_not_null_fields(self):
        data_dict = {
            'name': 'testproject1', 
            'date': datetime(2023, 5, 22),
            'test_project_group': 1
        }
        contains_all_unique_fields, contains_all_not_null_fields, all_not_null_fields_contain_data = self.manager._GeneralManager__isDataUploadable(data_dict, TestProject)
 
        self.assertFalse(contains_all_unique_fields)
        self.assertFalse(contains_all_not_null_fields)
        self.assertTrue(all_not_null_fields_contain_data)
 
    def test_is_data_uploadable_missing_data_in_not_null_fields(self):
        data_dict = {
            'name': 'testproject1', 
            'project_number': None,
            'date': datetime(2023, 5, 22),
            'test_project_group': 1
        }
        contains_all_unique_fields, contains_all_not_null_fields, all_not_null_fields_contain_data = self.manager._GeneralManager__isDataUploadable(data_dict, TestProject)
 
        self.assertTrue(contains_all_unique_fields)
        self.assertTrue(contains_all_not_null_fields)
        self.assertFalse(all_not_null_fields_contain_data)

class TestCheckInputDictForInvalidKeys(TestCase):
    def setUp(self):
        self.manager = GeneralManager.__new__(GeneralManager)
        self.group_model = TestProjectGroup
        self.data_model = TestProject
        self.manager._GeneralManager__group_model_name = 'test_project_group'

    def test_valid_keys(self):
        column_list = ['name', 'description', 'creator_id']
        invalid_key_list = ['date', 'group_id']

        self.manager._GeneralManager__checkInputDictForInvalidKeys(self.manager,column_list, invalid_key_list)

    def test_invalid_keys(self):
        column_list = ['date', 'name', 'group_id', 'creator_id']
        invalid_key_list = ['date', 'group_id']

        with self.assertRaises(ValueError):
            self.manager._GeneralManager__checkInputDictForInvalidKeys(self.manager,column_list, invalid_key_list)

class TestGetToCheckListForUpdate(TestCase):
    def setUp(self):
        self.manager = GeneralManager.__new__(GeneralManager)
        self.manager._GeneralManager__group_model_name = 'test_project_group'

    def test_get_to_check_list(self):
        expected_list = ['date', 'test_project_group', 'creator_id']
        actual_list = self.manager._GeneralManager__getToCheckListForUpdate()
        self.assertEqual(actual_list, expected_list)

class TestGetToCheckListForCreation(TestCase):
    def test_get_to_check_list(self):
        expected_list = ['date', 'creator_id']
        actual_list = GeneralManager._GeneralManager__getToCheckListForCreation()
        self.assertEqual(actual_list, expected_list)
        
class TestWriteDataData(TestCase):
    def setUp(self):
        GeneralManager.data_model = TestProject
        GeneralManager.group_model = TestProjectGroup
        self.manager = GeneralManager.__new__(GeneralManager)
        
        self.user = User.objects.create()
        self.test_project_group = TestProjectGroup.objects.create()
        self.test_project = TestProject.objects.create(
            name='TestProject1',
            project_number='123456',
            test_project_group = self.test_project_group,
            date = datetime(2023, 5, 15)
        )
    def test_write_data_data(self):
        latest_data = {
            'name': 'TestProject1',
            'project_number': '1234',
            'test_project_group': self.test_project_group,
            'date': self.test_project.date,
            'creator': self.user
        }
        data_data_dict = {
            'project_number': '1234567',
            'name' : 'TestProject2'
        }
        creator_id = self.user.id
        group_obj = self.test_project_group

        self.manager._GeneralManager__writeDataData(latest_data, data_data_dict, creator_id, group_obj)
        updated_data_obj = TestProject.objects.latest('id')
        self.assertEqual(updated_data_obj.project_number, '1234567')
        self.assertEqual(updated_data_obj.name, 'TestProject2')
        self.assertEqual(updated_data_obj.date.date(), datetime.now().date())
        self.assertEqual(updated_data_obj.creator, self.user)
        self.assertEqual(updated_data_obj.test_project_group, self.test_project_group)

class TestUpdate(TestCase):
    def setUp(self):
        self.user = User.objects.create(microsoft_id= 'a')
        self.test_project_group = TestProjectGroup.objects.create()
        self.test_project = TestProject.objects.create(
             name='TestProject1',
             project_number='123456',
             test_project_group=self.test_project_group,
             date= datetime(2023, 5, 15),
             creator = self.user
        )
        GeneralManager.group_model = TestProjectGroup
        GeneralManager.data_model = TestProject
        GeneralManager.data_extension_model_list = []
        self.manager = GeneralManager(group_id=self.test_project_group.id)
        self.manager.group_id = self.test_project_group.id
        self.manager._GeneralManager__group_obj = self.test_project_group
        self.manager._GeneralManager__group_model_name = 'test_project_group'
        self.manager.id = self.test_project.id
        self.creator_id = self.user.id

    def test_update(self):
        project_number_updated = '1234567890'
        self.manager.update(
            creator_id=self.creator_id, 
            project_number= project_number_updated
            )
        updated_data_obj = TestProject.objects.latest('id')
        self.assertEqual(updated_data_obj.project_number, '1234567890')
        
    def test_update_with_multiple_kwargs(self):
        project_number_updated = '1234567890'
        name_updated = 'TestProject1Updated'        

        self.manager.update(creator_id=self.creator_id, project_number= project_number_updated, name=name_updated)
        updated_data_obj = TestProject.objects.latest('id')
        self.assertEqual(updated_data_obj.project_number, '1234567890') 
        self.assertEqual(updated_data_obj.name, 'TestProject1Updated')

    def test_update_changing_date(self):
        date_updated = datetime.now()
        with self.assertRaises(ValueError):
           self.manager.update(creator_id=self.creator_id, date = date_updated)
        
    def test_update_changing_group_id(self):
        new_group = TestProjectGroup.objects.create()
        group_updated = new_group.id
        with self.assertRaises(ValueError):
           self.manager.update(creator_id=self.creator_id, group_id = group_updated )

class TestDeactivate(TestCase):
    def setUp(self):
        self.manager = GeneralManager.__new__(GeneralManager)
        GeneralManager.group_model = TestProjectGroup
        GeneralManager.data_model = TestProject2
        GeneralManager.data_extension_model_list = []

        self.user = User.objects.create(microsoft_id= 'a')
        self.test_project_group = TestProjectGroup.objects.create()
        self.test_project = TestProject2.objects.create(
             name='TestProject1',
             project_number='123',
             test_project_group=self.test_project_group,
             date=datetime(2023, 5, 15),
             creator = self.user,
             active = True
        )
        self.creator_id = self.user.id
        self.manager = GeneralManager(
            group_id=self.test_project_group.id
            )

    def test_deactivate(self):
        self.assertTrue(self.test_project.active)
        self.manager.deactivate(creator_id=self.creator_id)
        deactivated_data_obj = TestProject2.objects.latest('id')
        self.assertFalse(deactivated_data_obj.active)

    def test_deactivate_twice(self):
        self.manager.deactivate(creator_id=self.creator_id)
        with self.assertRaises(NotUpdatableError):
            self.manager.deactivate(creator_id=self.creator_id)

class TestCreate(TestCase):
    def setUp(self):
        self.manager = GeneralManager.__new__(GeneralManager)
        GeneralManager.group_model = TestProjectGroup2
        GeneralManager.data_model = TestProject3
        GeneralManager.data_extension_model_list = []

        self.user = User.objects.create(microsoft_id= 'a')
        self.creator_id = self.user.id
        self.test_project_group2 = TestProjectGroup2.objects.create(
            unique1 = 'a',
            unique2 = 'a'
        )
        self.test_project = TestProject3.objects.create(
             name='TestProject1',
             project_number='123',
             test_project_group2=self.test_project_group2,
             date=datetime(2023, 5, 15),
             creator = self.user,
             active = True
        )
        self.test_project_user_group2 = TestProjectUserGroup2.objects.create(
            unique1ProjectUserGroup = 'a',
            unique2ProjectUserGroup = 'a'
        )
        self.test_project_user_role1 = TestProjectUserRole.objects.create(role_name='Role 1')
        self.test_project_user_role2 = TestProjectUserRole.objects.create(role_name='Role 2')

    def test_create_new(self):
        group_data = {
            "unique1": 'a',
            "unique2": 'b'
        }
        data_data = {
            'name': 'TestProjectNew',
            'project_number': '123456New',
            'ap_no': 1,
            'test_project_group2' : self.test_project_group2,
        }
        
        def dummy_init(self, group_id, search_date=None):
            self.group_id = group_id
            self.active = 1
            self.start_date = datetime.now()
            self.search_date = search_date
        with patch.object(GeneralManager, '__init__', new = dummy_init):
            self.manager.create(self.creator_id, **group_data, **data_data)

            group_entries = TestProjectGroup2.objects.count()
            data_entries = TestProject3.objects.count()
            self.assertEqual(group_entries,2)
            self.assertEqual(data_entries,2)

            created_data = TestProject3.objects.latest('id')
            self.assertEqual(created_data.name, 'TestProjectNew')
            self.assertEqual(created_data.project_number, '123456New')
            self.assertEqual(created_data.test_project_group2, TestProjectGroup2.objects.get(id=2))
            self.assertTrue(created_data.active)

    def test_create_not_new(self):
        creator_id = self.creator_id
        group_data = {
            "unique1": 'a',
            "unique2": 'a'
        }
        data_data = {
            'name': 'TestProjectNew',
            'project_number': '123456New',
            'ap_no': None
        }

        def dummy_init(self, group_id, search_date=None):
            self.group_id = group_id
            self.active = 1
            self.start_date = datetime.now()
            self.search_date = search_date
        with patch.object(GeneralManager, '__init__', new = dummy_init):
            self.manager.create(creator_id, **group_data, **data_data)

            group_entries = TestProjectGroup2.objects.count()
            data_entries = TestProject3.objects.count()
            self.assertEqual(group_entries,1)
            self.assertEqual(data_entries,2)

            created_data = TestProject3.objects.latest('id')
            self.assertEqual(created_data.name, 'TestProjectNew')
            self.assertEqual(created_data.project_number, '123456New')
            self.assertEqual(created_data.test_project_group2, self.test_project_group2)
            self.assertTrue(created_data.active)

    def test_create_many_to_many_relation_with_existing_group_id(self):
        
        self.manager = GeneralManager.__new__(GeneralManager)
        GeneralManager.group_model = TestProjectUserGroup2
        GeneralManager.data_model = TestProjectUser2

        creator_id = self.creator_id
        group_data = {
            'unique1ProjectUserGroup': 'a',
            'unique2ProjectUserGroup': 'a'
        }
        data_data = {
            'test_project_user_role_id_list': [self.test_project_user_role1.id, self.test_project_user_role2.id],
            'creator': self.user,
            'active': 1,
            'name': 'TestProjectUserNew'
        }

        def dummy_init(self, group_id, search_date=None):
            self.group_id = group_id
            self.active = 1
            self._start_date = datetime.now()
            self.search_date = search_date

        with patch.object(GeneralManager, '__init__', new = dummy_init):
            self.manager.create(creator_id, **group_data, **data_data)

            group_entries = TestProjectUserGroup2.objects.count()
            data_entries = TestProjectUser2.objects.count()
            self.assertEqual(group_entries,1)
            self.assertEqual(data_entries,1)

            created_data = TestProjectUser2.objects.latest('id')
            self.assertEqual(created_data.name, 'TestProjectUserNew')
            self.assertEqual(created_data.test_project_user_group2, self.test_project_user_group2)
            self.assertTrue(created_data.active)

            self.assertEqual(created_data.test_project_user_role.count(), 2)
            self.assertTrue(created_data.test_project_user_role.filter(role_name='Role 1').exists())
            self.assertTrue(created_data.test_project_user_role.filter(role_name='Role 2').exists())

    def test_create_many_to_many_relation_with_new_group_id(self):

        self.manager = GeneralManager.__new__(GeneralManager)
        GeneralManager.group_model = TestProjectUserGroup2
        GeneralManager.data_model = TestProjectUser2
        creator_id = self.creator_id

        group_data = {
            'unique1ProjectUserGroup': 'b',
            'unique2ProjectUserGroup': 'b'
        }
        data_data = {
            'test_project_user_role_id_list': [self.test_project_user_role1.id, self.test_project_user_role2.id],
            'creator': self.user,
            'active': 1,
            'name': 'TestProjectUserNew'
        }

        def dummy_init(self, group_id, search_date=None):
            self.group_id = group_id
            self.active = 1
            self._start_date = datetime.now()
            self.search_date = search_date

        with patch.object(GeneralManager, '__init__', new = dummy_init):
            self.manager.create(creator_id, **group_data, **data_data)

            group_entries = TestProjectUserGroup2.objects.count()
            data_entries = TestProjectUser2.objects.count()
            self.assertEqual(group_entries,2)
            self.assertEqual(data_entries,1)

            created_data = TestProjectUser2.objects.latest('id')
            self.assertEqual(created_data.name, 'TestProjectUserNew')
            self.assertEqual(created_data.test_project_user_group2, TestProjectUserGroup2.objects.get(id=2))
            self.assertTrue(created_data.active)

            self.assertEqual(created_data.test_project_user_role.count(), 2)
            self.assertTrue(created_data.test_project_user_role.filter(role_name='Role 1').exists())
            self.assertTrue(created_data.test_project_user_role.filter(role_name='Role 2').exists())

    def test_create_no_corresponding_column_in_dict(self):
        creator_id = self.creator_id
        group_data = {
            "unique1": 'a',   
            "unique2": 'a'
        }
        data_data = {
            'name': 'TestProjectNew',
            'project_number': '123456New',
            'ap_no': None,
            'test_project_group' : self.test_project_group2
        }

        with self.assertRaises(ValueError): 
            self.manager.create(creator_id, **group_data, **data_data)   
    
    
class TestGetRefAndTableType(TestCase):

    def test_related_model(self):
        field = TestProject._meta.get_field('test_project_group')
        ref_table_type, ref_type = GeneralManager._GeneralManager__getRefAndTableType(field)
        self.assertEqual(ref_table_type, 'GroupTable')
        self.assertEqual(ref_type, 'ForeignKey')

    def test_non_related_model(self):
        field = TestProject._meta.get_field('name')
        ref_table_type, ref_type = GeneralManager._GeneralManager__getRefAndTableType(field)
        self.assertIsNone(ref_table_type)
        self.assertIsNone(ref_type)

    def test_many_to_many_field(self):
        field = TestProjectUser._meta.get_field('test_project_user_role')
        ref_table_type, ref_type = GeneralManager._GeneralManager__getRefAndTableType(field)
        self.assertEqual(ref_table_type, 'ReferenceTable')
        self.assertEqual(ref_type, 'ManyToManyField') 

    def test_many_to_one_field(self):
        pass


class TestCheckIfColumnReferencesDataExtensionModel(TestCase):
  
    def setUp(self):   
        self.column_name = 'project_dict_list'
        self.possible_models = {'TestProject', 'TestProjectGroup','project', 'Patent'}

    def test_check_if_column_references_data_extension_model(self):                                      
        result = GeneralManager._GeneralManager__checkIfColumnReferencesDataExtensionModel(self.column_name, self.possible_models)
        self.assertEqual(result,('project',True))
  
    def test_check_if_column_references_non_existing_data_extension_model(self):                                      
        result = GeneralManager._GeneralManager__checkIfColumnReferencesDataExtensionModel('nonexistent_column', self.possible_models)
        self.assertEqual(result,('nonexistent_column',False))

    def test_column_name_not_in_possible_models(self):
        result = GeneralManager._GeneralManager__checkIfColumnReferencesDataExtensionModel('project_dict_list', [])
        self.assertEqual(result, ('project_dict_list', False))

    def test_column_name_empty(self):
        result = GeneralManager._GeneralManager__checkIfColumnReferencesDataExtensionModel('', self.possible_models)
        self.assertEqual(result, ('', False))

    def test_column_wrong_column_name_ending(self):
        result = GeneralManager._GeneralManager__checkIfColumnReferencesDataExtensionModel('project_id_list', self.possible_models)
        self.assertEqual(result, ('project_id_list', False))


class TestErrorForInsufficientUploadData(TestCase):
    def setUp(self):
        GeneralManager.group_model = TestProjectGroup
        GeneralManager.data_model = TestProject
        self.manager = GeneralManager.__new__(GeneralManager)
        self.model_type = 'data_model'
        self.is_data_uploadable_with_error = [True, False, True]
        self.is_data_uploadable_without_error = [True, True, True]

    def test_error_with_error(self):
        with self.assertRaises(ValueError):
            self.manager._GeneralManager__errorForInsufficientUploadData(self.model_type, self.is_data_uploadable_with_error)

    def test_error_with_error(self):
        with self.assertRaises(ValueError):
            self.manager._GeneralManager__errorForInsufficientUploadData(self.model_type, self.is_data_uploadable_without_error)


class TestIsDataTableDataUploadable(TestCase):
    def setUp(self):
        GeneralManager.group_model= TestProjectGroup
        GeneralManager.data_model = TestProject2
        self.manager = GeneralManager.__new__(GeneralManager)

    def test_data_uploadable(self):
        data_data_dict = {
            'name': 'testproject1',
            'project_number': '123456',
            'date': datetime(2023, 5, 22),
            'test_project_group': 1,
            'ap_no' : 2
        }
        self.assertTrue(self.manager._GeneralManager__isDataTableDataUploadable(data_data_dict))

    def test_missing_unique_fields(self):
        data_data_dict = {
            'name': 'testproject1',
            # 'project_number': '123456',
            'date': datetime(2023, 5, 22),
            'test_project_group': 1,
            'ap_no' : 2
        }
        with self.assertRaises(ValueError):
            self.manager._GeneralManager__isDataTableDataUploadable(data_data_dict)

    def test_missing_not_null_fields(self):
        data_data_dict = {
            'name': 'testproject1',
            'date': datetime(2023, 5, 22),
            'test_project_group': 1
        }
        with self.assertRaises(ValueError):
            self.manager._GeneralManager__isDataTableDataUploadable(data_data_dict)

    def test_missing_data_in_not_null_fields(self):
        data_data_dict = {
            'name': 'testproject1',
            'project_number': None,
            'date': datetime(2023, 5, 22),
            'test_project_group': 1
        }
        with self.assertRaises(ValueError):
             self.manager._GeneralManager__isDataTableDataUploadable(data_data_dict)


class TestIsGroupTableDataUploadable(TestCase):
    def setUp(self):
        GeneralManager.group_model = TestProjectGroup2
        GeneralManager.data_model = TestProject2
        self.manager = GeneralManager.__new__(GeneralManager)

    def test_data_uploadable(self):
        group_data_dict = {
            'unique1': 'u1',
            'unique2': 'u2',
        }
        self.assertTrue(self.manager._GeneralManager__isGroupTableDataUploadable(group_data_dict))

    def test_missing_unique_fields(self):
        group_data_dict = {
            'unique1': 'u1',
            #'unique2': 'u2',
        }
        with self.assertRaises(ValueError):
            self.manager._GeneralManager__isGroupTableDataUploadable(group_data_dict)

    def test_missing_not_null_fields(self):
        group_data_dict = {}
        with self.assertRaises(ValueError):
            self.manager._GeneralManager__isGroupTableDataUploadable(group_data_dict)

    def test_missing_data_in_not_null_fields(self):
        group_data_dict = {
            'unique1': None,
            'unique2': 'u2',
        }
        with self.assertRaises(ValueError):
            self.manager._GeneralManager__isGroupTableDataUploadable(group_data_dict)


class TestGetEndDate(TestCase):
    def setUp(self):
        GeneralManager.group_model = TestProjectGroup
        GeneralManager.data_model = TestProject
        self.manager = GeneralManager.__new__(GeneralManager)
        self.manager._GeneralManager__group_model_name = 'test_project_group'
        self.test_project_group = TestProjectGroup.objects.create()
        self.manager._GeneralManager__group_obj = self.test_project_group
        self.manager._start_date = datetime(2023, 5, 15)


    def test_get_end_date_with_newer_entry(self):
        older_date = datetime(2023, 5, 15)
        older_data = self.manager.data_model.objects.create(
            test_project_group=self.test_project_group,
            date=older_date,
            project_number = '123'
        )
        newer_date = datetime(2023, 5, 16)
        newer_data = self.manager.data_model.objects.create(
            test_project_group=self.test_project_group,
            date=newer_date,
            project_number = '321'
        )
        # Check if __getEndDate returns the newer date
        self.assertEqual(self.manager._GeneralManager__getEndDate(), newer_date)

    def test_get_end_date_without_newer_entry(self):
        older_date = datetime(2023, 5, 15)
        older_data = self.manager.data_model.objects.create(
            test_project_group=self.test_project_group,
            date=older_date
        )
        # Check if __getEndDate returns None when there is no newer entry
        self.assertIsNone(self.manager._GeneralManager__getEndDate())


class TestGetOrCreateGroupModel(TestCase):
    def setUp(self):

        GeneralManager.group_model = TestProjectGroup2
        self.manager = GeneralManager.__new__(GeneralManager)

    def test_get_or_create_group_model_with_unique_fields(self):
        group_data_dict = {
            'unique1': 'u1',
            'unique2': 'u2',
        }
        # Ensure that the group model is not already in the database
        self.assertEqual(TestProjectGroup2.objects.filter(**group_data_dict).count(), 0)
        group_obj = self.manager._GeneralManager__getOrCreateGroupModel(group_data_dict)

        self.assertIsInstance(group_obj, TestProjectGroup2)
        self.assertTrue(group_obj.pk)
        self.assertEqual(group_obj.unique1, 'u1')
        self.assertEqual(group_obj.unique2, 'u2')

    def test_get_or_create_group_model_without_unique_fields(self):
        GeneralManager.group_model = TestProjectGroup3
        group_data_dict = {
            'unique3': 'u3',
            'unique4': 'u4',
        }
        self.assertEqual(TestProjectGroup3.objects.filter(**group_data_dict).count(), 0)
        group_obj = self.manager._GeneralManager__getOrCreateGroupModel(group_data_dict)
        self.assertIsInstance(group_obj, TestProjectGroup3)
        self.assertTrue(group_obj.pk)
        self.assertEqual(group_obj.unique3, 'u3')
        self.assertEqual(group_obj.unique4, 'u4')

    def test_get_existing_group_model(self):
        existing_group = TestProjectGroup2.objects.create(unique1='u1', unique2='u2')
        group_data_dict = {
            'unique1': 'u1',
            'unique2': 'u2',
        }
        self.assertEqual(TestProjectGroup2.objects.filter(**group_data_dict).count(),1)

        group_obj = self.manager._GeneralManager__getOrCreateGroupModel(group_data_dict)
        self.assertIsInstance(group_obj, TestProjectGroup2)
        self.assertEqual(group_obj.id, existing_group.id)
        self.assertEqual(group_obj.unique1, 'u1')
        self.assertEqual(group_obj.unique2, 'u2')


class TestGetDataExtensionData(TestCase):
    def setUp(self):
        GeneralManager.group_model = TestProjectGroup
        GeneralManager.data_model = TestProject2
        self.manager = GeneralManager.__new__(GeneralManager)
        self.manager.group_id = 1
        self.manager._GeneralManager__group_model_name = 'test_project_group'
        GeneralManager.data_extension_model_list = [TestProject2ExtensionTable]
        self.test_project_group = TestProjectGroup.objects.create()
        self.test_project_2 = TestProject2.objects.create(
            name ='testproject2',
            project_number = '123456',
            date = datetime(2023, 5, 22),
            test_project_group = self.test_project_group,
            ap_no = 2,
        )

    def test_with_non_list_value(self):
        key = 'TestProject2ExtensionTable_dict_list'
        value = 'TestProject'
        result = self.manager._GeneralManager__getDataExtensionData(key, value)
        self.assertEqual(result, (False, key, value))

  
    def test_get_data_extension_data_with_non_list_value(self):
        key = 'TestProject2ExtensionTable_dict_list'
        value = 1
        is_in_data_ext_model, model_name, to_upload_dict = self.manager._GeneralManager__getDataExtensionData(key, value)
        
        self.assertFalse(is_in_data_ext_model)
        self.assertEqual(model_name, key)
        self.assertEqual(to_upload_dict, value)


    def test_getDataExtensionData_with_data_extension_model(self):
        key = 'TestProject2ExtensionTable_dict_list'
        value = [
            {'name_extension' : 'extension1'},
            {'name_extension' : 'extension2'}
        ]

        is_in_data_ext_model, model_name, to_upload_dict =self.manager._GeneralManager__getDataExtensionData(
            key, value
        )
        self.assertTrue(is_in_data_ext_model)
        self.assertEqual(model_name, 'TestProject2ExtensionTable')
        self.assertIsInstance(to_upload_dict, dict)
        self.assertEqual(to_upload_dict['referenced_model'], TestProject2ExtensionTable)
        self.assertEqual(len(to_upload_dict['data']), 2)


    def test_with_invalid_column_in_value(self):
        key = 'TestProject2ExtensionTable_dict_list'
        value = [
            {'invalid_column': 'Invalid'}
        ]
        with self.assertRaises(ValueError):
            self.manager._GeneralManager__getDataExtensionData(key, value)


    def test_get_data_extension_data_with_invalid_model(self):
        key = 'NoneExistingModel'
        value = [
            {'name_extension' : 'extension1'},
            {'name_extension' : 'extension2'}
        ]
        is_in_data_ext_model, model_name, to_upload_dict = (self.manager._GeneralManager__getDataExtensionData(key, value))
        is_in_data_ext_model, model_name, to_upload_dict
        self.assertFalse(is_in_data_ext_model)
        self.assertEqual('NoneExistingModel', key)
        self.assertEqual(to_upload_dict, value)


class TestCheckIfDataExtensionIsUploadable(TestCase):
    def setUp(self):
        GeneralManager.group_model = TestProjectGroup
        GeneralManager.data_model = TestProject
        GeneralManager.data_extension_model_list = [TestProject2ExtensionTable]
        self.manager = GeneralManager.__new__(GeneralManager)
        test_project_group = TestProjectGroup.objects.create()
        self.test_project2 = TestProject2.objects.create(
            test_project_group = test_project_group
        )

    def test_data_extension_uploadable(self):
        data_extension_model = TestProject2ExtensionTable
        data_extension_data_dict = {
            'TestProject2ExtensionTable':   
                {
                    'name_extension': 'extension1',
                    'name_extension' : 'extension2',
                    'price': 45,
                    'test_project2' : self.test_project2
                }
        }
        self.assertTrue(
            self.manager._GeneralManager__checkIfDataExtensionIsUploadable(
                data_extension_model, data_extension_data_dict
            )
        )

    def test_missing_data_extension_model(self):
        data_extension_model = TestProject2ExtensionTable
        data_extension_data_dict = {}
        self.assertFalse(
            self.manager._GeneralManager__checkIfDataExtensionIsUploadable(
                data_extension_model, data_extension_data_dict
            )
        ) 

    def test_incomplete_data_extension_data(self):
        data_extension_model = TestProject2ExtensionTable
        data_extension_data_dict = {
            'TestProject2ExtensionTable':  
                {
                    'name_extension': 'extension1',
                    #'price': 45
                }
        }
        with self.assertRaises(ValueError):
            self.manager._GeneralManager__checkIfDataExtensionIsUploadable(
                data_extension_model, data_extension_data_dict
            )
       
    def test_invalid_data_extension_data(self):
        data_extension_model = TestProject2ExtensionTable
        data_extension_data_dict = {
            'TestProject2ExtensionTable':   
                {
                    'name_extension': 'extension1',
                    'invalid_field' : 'invalid_value',
                }
        }
        self.assertFalse(
            self.manager._GeneralManager__checkIfDataExtensionIsUploadable(
                data_extension_model, data_extension_data_dict
            )
        )

 
class TestIsDataExtensionTableDataUploadable(TestCase):
    def setUp(self):
        self.manager = GeneralManager.__new__(GeneralManager)

    def test_data_extension_table_data_uploadable(self):
        data_extension_data_dict = {
            'TestProject2ExtensionTable':   
                {
                    'name_extension': 'extension1',
                    'price': 45
                }
        }
    
        result = self.manager._GeneralManager__isDataExtensionTableDataUploadable(data_extension_data_dict)
        self.assertTrue(result)

    def test_data_extension_table_data_not_uploadable_missing_fields(self):
        data_extension_data_dict = {
            'TestProject2ExtensionTable':   
                {
                    'name_extension': 'extension1',
                    #'price': 45
                }
        }
        with self.assertRaises(ValueError):
            self.manager._GeneralManager__isDataExtensionTableDataUploadable(data_extension_data_dict)

    def test_data_extension_table_data_not_uploadable_invalid_data(self):
        data_extension_data_dict = {
            'TestProject2ExtensionTable':   
                {
                    'invalid_field' : 'invalid_value',
                }
        }

        result = self.manager._GeneralManager__isDataExtensionTableDataUploadable(data_extension_data_dict)
        self.assertFalse(result)
        

class TestGetToPushListForDataExtensionData(TestCase):
    def setUp(self):
        GeneralManager.data_extension_model_list = [TestProject2ExtensionTable]
        self.manager = GeneralManager.__new__(GeneralManager)


    def test_get_to_push_list_for_data_extension_data(self):
        data_extension_data_dict = {
            'TestProject2ExtensionTable': [  
                {
                    'name_extension': 'extension1',
                    'price': 22
                }
            ]
        }
        latest_extension_data = {
            'TestProject2ExtensionTable': [  
                {
                    'name_extension': 'extensionOld',
                    'price': 20
                }
            ]
        }
        result_list = self.manager._GeneralManager__getToPushListForDataExtensionData(
            TestProject2ExtensionTable, 
            data_extension_data_dict, 
            latest_extension_data,  
            TestProject2  
        )

        expected_result = [
            {
             'model_base': TestProject2 , 
             'name_extension': 'extension1',
             'price': 22,
            }
        ]
        self.assertEqual(result_list, expected_result)


class TestSaveDataToDB(TestCase):
    def setUp(self):
        GeneralManager.group_model = TestProjectGroup
        GeneralManager.data_model = TestProject2
        GeneralManager.data_extension_model_list = [TestProject2ExtensionTable]
        self.manager = GeneralManager.__new__(GeneralManager)

    def test_save_data_to_db(self):
        new_data_model_obj = TestProject2(
            name='Test Project 1',
            project_number='123456',
            test_project_group=TestProjectGroup.objects.create(),
            date=datetime(2023, 5, 22),
            ap_no=2,
            creator=User.objects.create(),
            active=True
        )

        saved_data_model_obj = self.manager._GeneralManager__saveDataToDB(
            TestProject2, 
            {
                'name': 'Test Project 1',
                'project_number': '123456',
                'test_project_group': new_data_model_obj.test_project_group,
                'date': datetime(2023, 5, 22),
                'ap_no': 2,
                'creator': new_data_model_obj.creator,
                'active': True
            }
        )
        self.assertEqual(saved_data_model_obj.name, 'Test Project 1')
        self.assertEqual(saved_data_model_obj.project_number, '123456')
        self.assertEqual(saved_data_model_obj.test_project_group.id, new_data_model_obj.test_project_group.id)
        self.assertEqual(saved_data_model_obj.date, datetime(2023, 5, 22))
        self.assertEqual(saved_data_model_obj.ap_no, 2)
        self.assertEqual(saved_data_model_obj.creator.id, new_data_model_obj.creator.id)
        self.assertTrue(saved_data_model_obj.active)       


class TestWriteDataExtensionData(TestCase):
    def setUp(self):
        GeneralManager.data_extension_model_list = [TestProject2ExtensionTable]
        self.manager = GeneralManager.__new__(GeneralManager)
        self.test_project_group = TestProjectGroup.objects.create()

    def test_write_data_extension_data(self):

        new_data_model_obj = TestProject2(
            name='Test Project 1',
            project_number='123456',
            test_project_group=self.test_project_group,
            date=datetime(2023, 5, 22),
            ap_no=2,
            creator= User.objects.create(),
            active=True
        )
        new_data_model_obj.save()

        data_extension_data_dict = {
            'TestProject2ExtensionTable': [  
                {
                    'name_extension': 'extension1',
                    'price': 23
                }
            ]
        }
        self.manager._GeneralManager__writeDataExtensionData(
            {}, 
            data_extension_data_dict,
            new_data_model_obj
        )
        data_extension_model = TestProject2ExtensionTable.objects.get(id=1)
        self.assertEqual(data_extension_model.name_extension, 'extension1')
        self.assertEqual(data_extension_model.price, 23)

    def test_write_data_extension_data_with_latest_extension_data(self):

        new_data_model_obj = TestProject2(
            name='Test Project 1',
            project_number='123456',
            test_project_group=self.test_project_group,
            date=datetime(2023, 5, 22),
            ap_no=2,
            creator= User.objects.create(),
            active=True
        )
        new_data_model_obj.save()
        
        latest_extension_data = {
            'TestProject2ExtensionTable': [  
                {
                    'name_extension': 'extension1',
                    'price': 45
                }
            ]
        }
        data_extension_data_dict = {
            'TestProject2ExtensionTable': [  
                {
                    'name_extension': 'extensionNEW',
                    'price': 45
                }
            ]
        }
        self.manager._GeneralManager__writeDataExtensionData(
            latest_extension_data, 
            data_extension_data_dict,
            new_data_model_obj
        )
        data_extension_model = TestProject2ExtensionTable.objects.get(id=1)
        self.assertEqual(data_extension_model.name_extension, 'extensionNEW')
        self.assertEqual(data_extension_model.price, 45)


class TestGetLatestDataData(TestCase):
    def setUp(self):
        GeneralManager.data_extension_model_list = [TestProject2ExtensionTable]
        self.test_project_group = TestProjectGroup.objects.create()
        self.manager = GeneralManager.__new__(GeneralManager)
        self.manager._GeneralManager__group_obj = self.test_project_group
        self.manager.data_model = TestProject2
        self.manager.group_model = TestProjectGroup

    def test_get_latest_data_data_empty(self):
        self.assertEqual(TestProject2.objects.count(), 0)
        latest_data = self.manager._GeneralManager__getLatestDataData()
        self.assertEqual(latest_data, {})


    def test_get_latest_data_data(self):
        new_data_model_obj = TestProject2(
            name='Test Project 1',
            project_number='123456',
            test_project_group=self.test_project_group,
            date=datetime(2023, 5, 22),
            ap_no=2,
            creator=User.objects.create(),
            active=True
        )
        new_data_model_obj.save()

        latest_data = self.manager._GeneralManager__getLatestDataData()
        self.assertEqual(latest_data['name'], 'Test Project 1')
        self.assertEqual(latest_data['project_number'], '123456')
        self.assertEqual(latest_data['test_project_group_id'], new_data_model_obj.test_project_group.id)
        self.assertEqual(latest_data['date'], datetime(2023, 5, 22))
        self.assertEqual(latest_data['ap_no'], 2)
        self.assertEqual(latest_data['creator_id'], new_data_model_obj.creator.id)
        self.assertTrue(latest_data['active'])


class TestGetLatestDataExtensionData(TestCase):
    def setUp(self):
        GeneralManager.group_model = TestProjectGroup
        GeneralManager.data_model = TestProject2
        GeneralManager.data_extension_model_list = [TestProject2ExtensionTable]
        self.manager = GeneralManager.__new__(GeneralManager)

        self.test_project_group = TestProjectGroup.objects.create()
        self.test_project2 = TestProject2.objects.create(
            test_project_group = self.test_project_group
        )
        self.manager.group_id=self.test_project_group.id
        self.manager._GeneralManager__data_obj = self.test_project2
        
        
    def test_get_latest_data_extension_data(self):
        new_data_extension_model_obj = TestProject2ExtensionTable(
            name_extension='extension1',
            price=22,
            test_project2=self.test_project2,
        )
        new_data_extension_model_obj.save()
        
        latest_extension_data = self.manager._GeneralManager__getLatestDataExtensionData()
        self.assertEqual(latest_extension_data, {'TestProject2ExtensionTable' : [{'id':new_data_extension_model_obj.id ,'name_extension': 'extension1', 'price': 22, 'test_project2_id': self.test_project2.id}]})
         

    def test_get_latest_data_extension_data_empty(self):
        latest_extension_data = self.manager._GeneralManager__getLatestDataExtensionData()
        self.assertEqual(latest_extension_data, {'TestProject2ExtensionTable': []})   


class TestWriteData(TestCase):
    def setUp(self):
        self.creator_user = User.objects.create()
        GeneralManager.group_model = TestProjectGroup
        GeneralManager.data_model = TestProject2
        GeneralManager.data_extension_model_list = [TestProject2ExtensionTable]
        self.manager = GeneralManager.__new__(GeneralManager)
        self.test_project_group = TestProjectGroup.objects.create()

    def test_write_data_data(self):
        latest_data_data = {
            'name': 'TestProject1',
            'project_number': '123456',
            'ap_no': 11,
            'test_project_group': self.test_project_group,
            'creator': self.creator_user
        }

        data_data_dict = {
            'name': 'Test Project 1',
            'project_number': '123456',
            'ap_no': 12,
            'test_project_group': self.test_project_group,
            'creator': self.creator_user.id
        }
        latest_extension_data = {'TestProject2ExtensionTable': [{'name_extension': 'extension1'}]}
        data_extension_data_dict = {
            'TestProject2ExtensionTable': [
                {
                    'name_extension': 'extension1',
                    'price': 23
                }
            ]
        }
        new_data_model_obj = self.manager._GeneralManager__writeData(
            latest_data_data,
            data_data_dict,
            creator_id=self.creator_user.id,
            group_obj=self.test_project_group,
            latest_extension_data=latest_extension_data,
            data_extension_data_dict=data_extension_data_dict,
        )
        new_data_model_obj = TestProject2.objects.get(id=1)
        self.assertIsNotNone(new_data_model_obj.id)
        self.assertEqual(new_data_model_obj.name, 'Test Project 1')
        self.assertEqual(new_data_model_obj.project_number, '123456')
        self.assertEqual(new_data_model_obj.ap_no, 12)
        self.assertEqual(new_data_model_obj.test_project_group, self.test_project_group)
        self.assertEqual(new_data_model_obj.creator, self.creator_user)

        data_extension_model = TestProject2ExtensionTable.objects.get(id=1)
        self.assertEqual(data_extension_model.name_extension, 'extension1')
        self.assertEqual(data_extension_model.price, 23)


class TestGetFieldsAndValues(TestCase):
    def setUp(self):
        self.test_project_group = TestProjectGroup.objects.create()
        self.creator_user = User.objects.create()
        self.test_project = TestProject2.objects.create(
            name='Test Project 1',
            project_number='123456',
            test_project_group=self.test_project_group,
            date='2023-05-22',
            ap_no=2,
            creator=self.creator_user,
            active=True,
        )

    def test_get_fields_and_values(self):
        fields_and_values = GeneralManager._GeneralManager__getFieldsAndValues(self.test_project)
        self.assertIsInstance(fields_and_values, dict)
        self.assertEqual(fields_and_values['name'], 'Test Project 1')
        self.assertEqual(fields_and_values['project_number'], '123456')
        self.assertEqual(fields_and_values['test_project_group'], self.test_project_group)
        self.assertEqual(fields_and_values['date'], '2023-05-22')
        self.assertEqual(fields_and_values['ap_no'], 2)
        self.assertEqual(fields_and_values['creator'], self.creator_user)
        self.assertTrue(fields_and_values['active'])
       

    def test_get_fields_and_values_many_to_many(self):
            role1 = TestProjectUserRole.objects.create(role_name = 'role1')
            role2 = TestProjectUserRole.objects.create(role_name = 'role2')
            test_project_user_group = TestProjectUserGroup.objects.create()
            test_project_user = TestProjectUser.objects.create(
            test_project_user_group = test_project_user_group
            )
            test_project_user.test_project_user_role.add(role1)
            test_project_user.test_project_user_role.add(role2)

            fields = GeneralManager._GeneralManager__getFieldsAndValues(test_project_user)

            self.assertEqual(fields['test_project_user_group'], test_project_user_group)
            self.assertEqual(fields['test_project_user_role'], [role1, role2])


class TestCreateSearchKeys(TestCase):
    
    def test_valid_key_value(self):
        key = 'name'
        value = 'TestProject1'
        result = GeneralManager._GeneralManager__createSearchKeys(key, value)      

        expected_result = ('name', 'TestProject1')
        self.assertEqual(result, expected_result)

    def test_valid_key_tuple_value(self):
        key = 'ap_no'
        value = ['>', 5]
        result = GeneralManager._GeneralManager__createSearchKeys(key, value)      
        expected_result = ('ap_no__gt', 5)
        self.assertEqual(result, expected_result)

    def test_invalid_operator(self):
        key = 'project_number'
        value = ['!=', '123456']
        with self.assertRaises(ValueError):
            GeneralManager._GeneralManager__createSearchKeys(key, value)

    def test_invalid_tuple_length(self):
        key = 'date'
        value = ['>=', '2023-07-17', '2023-07-31']
        with self.assertRaises(ValueError):
            GeneralManager._GeneralManager__createSearchKeys(key, value)

    def test_invalid_operator_and_value(self):
        key = 'name'
        value = [None, 'TestProject1']
        with self.assertRaises(ValueError):
            GeneralManager._GeneralManager__createSearchKeys(key, value)





###### NEW ######################

class TestGetDataSourceAndColumnBaseName(TestCase):

    def setUp(self):
        GeneralManager.group_model = TestProjectGroup
        GeneralManager.data_model = TestProject2
        GeneralManager.data_extension_model_list = [TestProject2ExtensionTable]
        self.manager = GeneralManager.__new__(GeneralManager)


    def test_get_data_source_and_column_base_name_foreign_key(self):
        test_project = TestProject2.objects.create(
            name='Test Project',
            project_number='12345',
            test_project_group=TestProjectGroup.objects.create(),
            creator=None,
            ap_no=None,
            active=True,
        )
        column_name = TestProject2._meta.get_field('test_project_group')  
        ref_type = 'FOREIGNKEY' 
        ref_type = column_name.get_internal_type() 
       
        data_source, column_name = self.manager._GeneralManager__getDataSourceAndColumnBaseName(column_name, ref_type)
        expected_data_source = 'test_project_group'
        expected_column_name = 'test_project_group'
        self.assertEqual(column_name, expected_column_name)
        self.assertEqual(data_source, expected_data_source)
        

    def test_get_data_source_and_column_base_name_many_to_one(self):
        test_project2=TestProject2.objects.create(
                name='Test Project',
                project_number='12345',
                test_project_group=TestProjectGroup.objects.create(),
            )
        TestProject2ExtensionTable.objects.create(
            name_extension = 'Extension1',
            price=100,
            test_project2 = test_project2
        )
        column_name = TestProject2._meta.get_field('testproject2extensiontable')  
        ref_type = GeneralManager.MANY_TO_ONE 

        data_source, column_base_name = self.manager._GeneralManager__getDataSourceAndColumnBaseName(column_name, ref_type)

        expected_data_source = 'testproject2extensiontable_set' 
        expected_column_base_name = 'test_project2_extension_table'
        self.assertEqual(data_source, expected_data_source)
        self.assertEqual(column_base_name, expected_column_base_name)


    def test_get_data_source_and_column_base_name_many_to_many(self):
        role1 = TestProjectUserRole.objects.create(
            role_name = 'Role 1')
    
        test_project_user=TestProjectUser.objects.create(
                test_project_user_group=TestProjectUserGroup.objects.create(),
            )
        test_project_user.test_project_user_role.add(role1)

        column_name = TestProjectUser._meta.get_field('test_project_user_role')  
        ref_type = 'MANY_TO_MANY'  #ref_type = column_name.get_internal_type()

        data_source, column_base_name = self.manager._GeneralManager__getDataSourceAndColumnBaseName(column_name, ref_type)

        expected_data_source = 'test_project_user_role'
        expected_column_base_name = 'test_project_user_role'
        self.assertEqual(data_source, expected_data_source)
        self.assertEqual(column_base_name, expected_column_base_name)


class TestAssignAttribute(TestCase):
    def setUp(self):
        GeneralManager.group_model = TestProjectGroup
        GeneralManager.data_model = TestProject2
        GeneralManager.data_extension_model_list = [TestProject2ExtensionTable]
        self.manager = GeneralManager.__new__(GeneralManager)
        self.test_project_group = TestProjectGroup.objects.create()
        self.test_project_user_group = TestProjectUserGroup.objects.create()
        self.test_project_user_role1 = TestProjectUserRole.objects.create(role_name = 'role1')
        self.test_project_user_role2 = TestProjectUserRole.objects.create(role_name = 'role2')

    def test_assign_foreignkey_attribute(self):
        test_project = TestProject.objects.create(
            name='Test Project',
            project_number='12345',
            test_project_group=self.test_project_group,
            creator=None,
            active=True,
        )
        self.manager._GeneralManager__assignAttribute(TestProject._meta.get_field('test_project_group'), test_project)

        self.assertTrue(hasattr(self.manager, 'test_project_group'))
        self.assertEqual(self.manager.test_project_group, self.test_project_group)

    def test_assign_many_to_many_attribute(self):
        test_project_user = TestProjectUser.objects.create(
            test_project_user_group=self.test_project_user_group
        )
        test_project_user.test_project_user_role.add(self.test_project_user_role1, self.test_project_user_role2)

        self.manager._GeneralManager__assignAttribute(TestProjectUser._meta.get_field('test_project_user_role'), test_project_user)

        self.assertTrue(hasattr(self.manager, 'test_project_user_role'))
        self.assertEqual(set(self.manager.test_project_user_role.all()), {self.test_project_user_role1, self.test_project_user_role2})


class TestAssignExtensionDataDictAttribute(TestCase):
    def setUp(self):
        GeneralManager.group_model = TestProjectGroup
        GeneralManager.data_model = TestProject2
        GeneralManager.data_extension_model_list = [TestProject2ExtensionTable]
        self.manager = GeneralManager.__new__(GeneralManager)
        self.test_project_group = TestProjectGroup.objects.create()

    def test_assign_many_to_one_attribute(self):
        test_project = TestProject2.objects.create(
            name='Test Project',
            project_number='12345',
            test_project_group=self.test_project_group,
        )
        test_project_extension_data = TestProject2ExtensionTable.objects.create(
            name_extension='extension1',
            price=100,
            test_project2=test_project,
        )
        
        self.manager._GeneralManager__assignExtensionDataDictAttribute(
            TestProject2._meta.get_field('testproject2extensiontable'),
            test_project,
            GeneralManager.MANY_TO_ONE
        )

        attribute_name = 'test_project2_extension_table_dict_list'
        self.assertTrue(hasattr(self.manager, attribute_name))
        self.assertEqual(
            getattr(self.manager, attribute_name),
            [{
                'id': test_project_extension_data.id,
                'name_extension': 'extension1', 
                'price': 100,
                'test_project2': test_project
            },]
        )
        

class TestCreateDirectAttribute(TestCase):
    
    def setUp(self):
        self.manager = GeneralManager.__new__(GeneralManager)
        self.test_project_group = TestProjectGroup.objects.create()
        self.test_model_obj = TestProject2.objects.create(
            name='TestProject',
            project_number='1234',
            ap_no=42,
            test_project_group=self.test_project_group
        )
        self.data_extension = TestProject2ExtensionTable.objects.create(
            name_extension='Extension1',
            price=100,
            test_project2=self.test_model_obj
        )

    def test_create_direct_attribute_reference_table(self):
        column = TestProject2._meta.get_field('name')
        ref_table_type = 'ReferenceTable'
        ref_type = GeneralManager.FOREIGN_KEY  

        self.manager._GeneralManager__createDirectAttribute(
            ref_table_type,
            ref_type,
            column,
            self.test_model_obj
        )
        self.manager._GeneralManager__createDirectAttribute(
            ref_table_type,
            ref_type,
            TestProject2._meta.get_field('project_number'),
            self.test_model_obj
        )
        self.assertEqual(self.manager.name, 'TestProject')
        self.assertEqual(self.manager.project_number, '1234')

    # def test_create_direct_attribute_group_table(self):
    #     column = TestProject2._meta.get_field('test_project_group')
    #     ref_table_type = 'GroupTable'
    #     ref_type = GeneralManager.FOREIGN_KEY  

    #     self.manager._GeneralManager__createDirectAttribute(
    #         ref_table_type,
    #         ref_type,
    #         column,
    #         self.test_model_obj
    #     )
    #     self.assertEqual(self.manager.test_project_group, self.test_project_group)

    def test_create_direct_attribute_data_extension_table(self):
        column = TestProject2._meta.get_field('testproject2extensiontable')
        ref_table_type = 'DataExtensionTable'
        ref_type = GeneralManager.MANY_TO_ONE  

        self.manager._GeneralManager__createDirectAttribute(
            ref_table_type,
            ref_type,
            column,
            self.test_model_obj
        )
        self.assertEqual(self.manager.test_project2_extension_table_dict_list,  [{
                'id': self.data_extension.id,
                'name_extension': 'Extension1', 
                'price': 100,
                'test_project2': self.test_model_obj
            },])



class TestCreateProperty(TestCase):
    def setUp(self):
        self.manager = GeneralManager.__new__(GeneralManager)
    
    def test_create_property(self):
        def test_function(self):
            return "Test Django"
        self.manager._GeneralManager__createProperty('test_property', test_function)

        self.assertTrue(hasattr(self.manager, 'test_property'))
        self.assertEqual(self.manager.test_property, "Test Django")



class TestGetManagerFromGroupModel(TestCase):
    def setUp(self):
        self.manager = GeneralManager.__new__(GeneralManager)
        self.creator = User.objects.create()
        self.manager.search_date = datetime(2023,7,28)
        self.manager.use_cache = False

        self.new_kunden_group = newKundenGroup.objects.create()
        self.new_kunden = newKunden.objects.create(
            name= 'test1',
            new_kunden_group = self.new_kunden_group,
            date= datetime(2020, 1, 1),
            creator_id = self.creator.id
            )
        self.new_abc_group = newAbcGroup.objects.create()
        self.new_abc = newAbc.objects.create(
            new_abc_group = self.new_abc_group,
            date= datetime(2020, 2, 2),
            creator_id = self.creator.id
            )
        self.new_project_group = newProjectGroup.objects.create(new_abc_group= self.new_abc_group)
        self.new_project = newProject.objects.create(
            name='testProject',
            new_project_group = self.new_project_group,
            new_kunden = self.new_kunden,
            date= datetime(2020, 3, 3),
            creator_id = self.creator.id
            )

    def test_get_manager_from_group_model(self):
        column_name = 'new_abc_group_id'
        column = newProjectGroup._meta.get_field(column_name)
        model_obj = self.new_project_group
        ref_type = GeneralManager.FOREIGN_KEY

        method, attribute_name = self.manager._GeneralManager__getManagerFromGroupModel(
            column,
            model_obj,
            ref_type
        )
        setattr(self.new_project, column_name, self.new_project_group.id)
        self.new_project.save()

        result = method(self.manager)
        self.assertEqual(attribute_name, 'new_abc_manager')
        self.assertEqual(result.group_id, self.new_abc_group.id)
        self.assertEqual(result.search_date, datetime(2023,7,28))


class TestGetManagerFromDataModel(TestCase):
    def setUp(self):
        self.manager = GeneralManager.__new__(GeneralManager)
        self.creator = User.objects.create()
        self.manager.search_date = datetime(2023,7,28)
        self.manager.use_cache = False

        self.new_kunden_group = newKundenGroup.objects.create()
        self.new_kunden = newKunden.objects.create(
            name= 'test1',
            new_kunden_group = self.new_kunden_group,
            date= datetime(2020, 1, 1),
            creator_id = self.creator.id
            )
        self.new_abc_group = newAbcGroup.objects.create()
        self.new_abc = newAbc.objects.create(
            new_abc_group = self.new_abc_group,
            date= datetime(2020, 2, 2),
            creator_id = self.creator.id
            )
        self.new_project_group = newProjectGroup.objects.create(new_abc_group= self.new_abc_group)
        self.new_project = newProject.objects.create(
            name='testProject',
            new_project_group = self.new_project_group,
            new_kunden = self.new_kunden,
            date= datetime(2020, 3, 3),
            creator_id = self.creator.id
            )

    def test_get_manager_from_data_model(self):
        column_name = 'new_kunden_id'
        column = newProject._meta.get_field(column_name)
        model_obj = self.new_project
        ref_type = GeneralManager.FOREIGN_KEY

        method, attribute_name = self.manager._GeneralManager__getManagerFromDataModel(
            column,
            model_obj,
            ref_type
        )
        setattr(self.new_project, column_name, self.new_project_group.id)
        self.new_project.save()
        result = method(self.manager)
        self.assertEqual(attribute_name, 'new_kunden_manager')
        self.assertEqual(result.group_id, self.new_kunden.id)
        self.assertEqual(result.search_date, datetime(2023,7,28))


class TestGetManagerListFromGroupModel(TestCase):
    def setUp(self):
        GeneralManager.use_cache = False
        self.manager = GeneralManager.__new__(GeneralManager)
        self.creator = User.objects.create()
        self.manager.search_date = datetime(2023,7,28)

        self.new_kunden_group = newKundenGroup.objects.create()
        self.new_kunden = newKunden.objects.create(
            name= 'test1',
            new_kunden_group = self.new_kunden_group,
            date= datetime(2020, 1, 1),
            creator_id = self.creator.id
            )
        self.new_abc_group = newAbcGroup.objects.create()
        self.new_abc = newAbc.objects.create(
            new_abc_group = self.new_abc_group,
            date= datetime(2020, 2, 2),
            creator_id = self.creator.id
            )
        self.new_project_group = newProjectGroup.objects.create(new_abc_group= self.new_abc_group)
        self.new_project = newProject.objects.create(
            name='testProject',
            new_project_group = self.new_project_group,
            new_kunden = self.new_kunden,
            date= datetime(2020, 3, 3),
            creator_id = self.creator.id
            )
        self.new_project_user_group1 = newProjectUserGroup.objects.create(
            new_project_group = self.new_project_group
        )
        self.new_project_user_group2 = newProjectUserGroup.objects.create(
            new_project_group = self.new_project_group
        )
        self.new_project_user1 = newProjectUser.objects.create(
            new_project_user_group = self.new_project_user_group1,
            date= datetime(2020, 2, 2),
            creator_id = self.creator.id
        )
        self.new_project_user2 = newProjectUser.objects.create(
            new_project_user_group = self.new_project_user_group2,
            date= datetime(2020, 2, 3),
            creator_id = self.creator.id
        )
        self.new_project_user_role1 = newProjectUserRoles.objects.create(role='role1')
        self.new_project_user_role2 = newProjectUserRoles.objects.create(role='role2')
        self.new_project_user1.new_project_user_role.add(self.new_project_user_role1)
        self.new_project_user1.new_project_user_role.add(self.new_project_user_role2)


    def test_get_manager_from_group_model(self):
        column_name = 'newprojectusergroup'

        column = newProjectGroup._meta.get_field(column_name)
        model_obj = self.new_project_group
        ref_type = GeneralManager.MANY_TO_ONE
        

        method, attribute_name = self.manager._GeneralManager__getManagerListFromGroupModel(
            column,
            model_obj,
            ref_type
        )
        result = method(self.manager)
        self.assertEqual(attribute_name, 'new_project_user_manager_list')
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].group_id, self.new_project_user_group1.id)
        self.assertEqual(result[0].search_date, datetime(2023,7,28))
        self.assertEqual(result[1].group_id, self.new_project_user_group2.id)




class TestGetManagerListFromDataModel(TestCase):
    def setUp(self):
        self.manager = GeneralManager.__new__(GeneralManager)
        self.creator = User.objects.create()
        self.manager.search_date = datetime(2023,7,28)
        self.manager.use_cache = False

        self.new_kunden_group = newKundenGroup.objects.create()
        self.new_kunden = newKunden.objects.create(
            name= 'test1',
            new_kunden_group = self.new_kunden_group,
            date= datetime(2020, 1, 1),
            creator_id = self.creator.id
            )
        self.new_abc_group = newAbcGroup.objects.create()
        self.new_abc = newAbc.objects.create(
            new_abc_group = self.new_abc_group,
            date= datetime(2020, 2, 2),
            creator_id = self.creator.id
            )
        self.new_project_group = newProjectGroup.objects.create(new_abc_group= self.new_abc_group)
        self.new_project = newProject.objects.create(
            name='testProject',
            new_project_group = self.new_project_group,
            new_kunden = self.new_kunden,
            date= datetime(2020, 3, 3),
            creator_id = self.creator.id
            )
        self.new_project_user_group = newProjectUserGroup.objects.create(
            new_project_group = self.new_project_group
        )
        self.new_project_user = newProjectUser.objects.create(
            new_project_user_group = self.new_project_user_group,
            date= datetime(2020, 2, 2),
            creator_id = self.creator.id,
        )
        self.new_xyz_group = newXyzGroup.objects.create()
        self.new_xyz = newXyz.objects.create(
            new_xyz_group = self.new_xyz_group,
            date= datetime(2020, 2, 2),
            creator_id = self.creator.id
        )
        self.new_project_user_role1 = newProjectUserRoles.objects.create(role='role1')
        self.new_project_user_role2 = newProjectUserRoles.objects.create(role='role2')
        self.new_project_user.new_project_user_role.add(self.new_project_user_role1)
        self.new_project_user.new_project_user_role.add(self.new_project_user_role2)
        self.new_project_user.new_xyz.add(self.new_xyz)

    def test_get_manager_list_from_data_model(self):
        column_name = 'new_xyz'

        column = newProjectUser._meta.get_field(column_name)
        model_obj = self.new_project_user
        ref_type = GeneralManager.MANY_TO_MANY

        method, attribute_name = self.manager._GeneralManager__getManagerListFromDataModel(
            column,
            model_obj,
            ref_type
        )
        result = method(self.manager)
        self.assertEqual(attribute_name, 'new_xyz_manager_list')
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].group_id, self.new_project_user_group.id)
        self.assertEqual(result[0].search_date, datetime(2023,7,28))

    