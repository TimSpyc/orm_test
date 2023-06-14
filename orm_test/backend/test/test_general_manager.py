from unittest.mock import  Mock, patch
from backend.src.auxiliary.exceptions import NonExistentGroupError, NotUpdatableError, NotValidIdError
from django.test import TestCase
from backend.src.auxiliary.manager import GeneralManager
from datetime import date, datetime
from .models_for_testing import TestProjectGroup2, TestProject3, TestProject2, TestProjectGroup, TestProject, TestProjectUser2, TestProjectUserGroup, TestProjectUserGroup2, TestProjectUserRole, TestProjectUser
from backend.models import User
from django.core.exceptions import FieldDoesNotExist, FieldError


class TestProjectManager(GeneralManager):
    group_model = TestProjectGroup
    data_model = TestProject

    def __init__(self, test_project_group_id, search_date=None):
        group, data = super().__init__(
            group_id=test_project_group_id,
            search_date=search_date,
            )
class TestProjectUserManager(GeneralManager):
    group_model = TestProjectUserGroup
    data_model = TestProjectUser

    def __init__(self, test_project_user_group_id, search_date=None):
        group, data = super().__init__(
            group_id=test_project_user_group_id,
            search_date=search_date,
            )    

class TestSearchForColumn(TestCase):
    def setUp(self):
        self.column_list = ['name', 'description', 'start_date', 'end_date',  'owner', 'member']

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
        column_list = ['name', 'project_number', 'test_project_group_id']
        db_column = 'test_project_group_id'
        value = 1
        
        result = GeneralManager._GeneralManager__getValueAndColumnIfExists(db_column, column_list, model, value)
        # result = (is_in_model, db_column, value)
        self.assertEqual(result, (True, 'test_project_group_id', TestProjectGroup.objects.get(id=value).id))
        self.assertEqual(result, (True, 'test_project_group_id', 1))

    def test_column_exists_in_model(self):
        column_list = ['name', 'project_number', 'test_project_group_id']
        result = GeneralManager._GeneralManager__getValueAndColumnIfExists("name", column_list, TestProject, "example_value")
        self.assertEqual(result, (True, "name", "example_value"))

    def test_column_does_not_exist_in_model(self):
        column_list = ['name', 'project_number', 'test_project_group_id']
        result = GeneralManager._GeneralManager__getValueAndColumnIfExists("non_existent_column", column_list, TestProject, "example_value")
        self.assertEqual(result, (False, "non_existent_column", "example_value"))

    def test_get_value_and_column_if_exists_with_many_to_many_relation(self):
        column_list = ['test_project_user_group', 'test_project_user_role']
        value = [1, 2]
        is_in_model, db_column, value = GeneralManager._GeneralManager__getValueAndColumnIfExists('test_project_user_role_id_list', column_list, TestProjectUser, value)
        self.assertEqual((is_in_model, db_column, list(value)), (True, 'test_project_user_role', list(TestProjectUserRole.objects.filter(id__in=value))))

class TestGetColumnList(TestCase):

    @classmethod
    def setUpTestData(cls):
        project_group = TestProjectGroup.objects.create()
        TestProject.objects.create(
            name='TestProject1',
            project_number='123456',
            test_project_group = project_group
        )
    def test_get_column_list(self):
        result = GeneralManager._GeneralManager__getColumnList(TestProject)
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
        self.manager = TestProjectManager(test_project_group_id = self.test_project_group.id)
    
    def test_filter_with_search_date(self):
        search_date = date(2023, 5, 16)
        result = self.manager.filter(search_date=search_date)

        expected_result = [
            TestProjectManager(test_project_group_id= self.test_project_group.id, search_date= search_date)
        ]
        self.assertEqual(result, expected_result)

        
    def test_filter_with_invalid_filter_condition(self):
        with self.assertRaises(ValueError):
            result = self.manager.filter(invalid_field='invalid_value')


    def test_filter_with_other_filter_condition_than_searchDate(self):
        name = 'TestProject1'
        result = self.manager.filter(name = name)
        expected_result = [
            TestProjectManager(test_project_group_id= self.test_project_group.id)
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
            TestProjectManager(test_project_group_id=self.test_project_group.id, search_date = search_date)
        ]
        self.assertEqual(result, expected_result)


    def test_filter_with_many_to_many_relations(self):
        self.test_project_user_group = TestProjectUserGroup.objects.create()
        self.test_project_user_role1 = TestProjectUserRole.objects.create(role_name='Role 1')
        self.test_project_user_role2 = TestProjectUserRole.objects.create(role_name='Role 2')

        User.objects.all().delete()
        self.user = User.objects.create()

        self.test_project_user1 = TestProjectUser.objects.create(test_project_user_group = self.test_project_user_group, creator = self.user)
        self.test_project_user1.test_project_user_role.add(self.test_project_user_role1)
        self.test_project_user1.test_project_user_role.add(self.test_project_user_role2)

        
        self.many_to_many_manager = TestProjectUserManager(test_project_user_group_id=self.test_project_user_group.id)

        result = self.many_to_many_manager.filter(test_project_user_role = self.test_project_user_role1)
        expected_result = [
            TestProjectUserManager(test_project_user_group_id= self.test_project_user_group.id)
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
        self.manager = TestProjectManager(test_project_group_id = self.test_project_group.id)
    
    def test_all_with_search_date(self):
        search_date = date(2023, 5, 17)
        result = self.manager.all(search_date=search_date)

        expected_result = [
            TestProjectManager(test_project_group_id= self.test_project_group.id, search_date= search_date)
        ]
        self.assertEqual(result, expected_result)

    def test_all_without_search_date(self):
        result = self.manager.all()

        expected_result = [
            TestProjectManager(test_project_group_id= self.test_project_group.id),
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
        group_data_dict, data_data_dict = self.manager._GeneralManager__getDataForGroupAndDataTableByKwargs(   
            # self.manager,
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
                #self.manager,
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
                #self.manager,
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
            {'test_project_group_id': project_group1.id, 'search_date': search_date}
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
            {'test_project_group_id': project_group1.id, 'search_date': search_date}
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
                {'test_project_group_id': project_group1.id, 'search_date': None},
                {'test_project_group_id': project_group2.id, 'search_date': None}
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
            {'test_project_group_id': project_group1.id, 'search_date': search_date}
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
        group_id = 1
        group_obj = TestProjectGroup.objects.create(id=group_id)
 
        result = self.manager._GeneralManager__getGroupObject(group_id)
        self.assertEqual(result, group_obj)
 
    def test_with_invalid_group_id(self):
        non_existing_group_id = 12
        with self.assertRaises(NotUpdatableError):
            self.manager._GeneralManager__getGroupObject(non_existing_group_id)

class TestGetDataObject(TestCase):
    def setUp(self):
        self.manager = GeneralManager.__new__(GeneralManager)
        self.group_model = TestProjectGroup
        self.data_model = TestProject

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
        column_list = ['name', 'description', 'creator_user_id']
        invalid_key_list = ['date', 'group_id']

        self.manager._GeneralManager__checkInputDictForInvalidKeys(self.manager,column_list, invalid_key_list)

    def test_invalid_keys(self):
        column_list = ['date', 'name', 'group_id', 'creator_user_id']
        invalid_key_list = ['date', 'group_id']

        with self.assertRaises(ValueError):
            self.manager._GeneralManager__checkInputDictForInvalidKeys(self.manager,column_list, invalid_key_list)

class TestGetToCheckListForUpdate(TestCase):
    def setUp(self):
        self.manager = GeneralManager.__new__(GeneralManager)
        self.manager._GeneralManager__group_model_name = 'test_project_group'

    def test_get_to_check_list(self):
        expected_list = ['date', 'test_project_group', 'creator_user_id']
        actual_list = self.manager._GeneralManager__getToCheckListForUpdate()
        self.assertEqual(actual_list, expected_list)

class TestGetToCheckListForCreation(TestCase):
    def test_get_to_check_list(self):
        expected_list = ['date', 'creator_user_id']
        actual_list = GeneralManager._GeneralManager__getToCheckListForCreation()
        self.assertEqual(actual_list, expected_list)
        
class TestWriteDataData(TestCase):
    def setUp(self):
        self.manager = GeneralManager.__new__(GeneralManager) 
        self.manager.group_model = TestProjectGroup
        self.manager.data_model = TestProject
        
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
        creator_user_id = self.user.id
        group_obj = self.test_project_group

        self.manager._GeneralManager__writeDataData(latest_data, data_data_dict, creator_user_id, group_obj)
        updated_data_obj = TestProject.objects.latest('id')
        self.assertEqual(updated_data_obj.project_number, '1234567')
        self.assertEqual(updated_data_obj.name, 'TestProject2')
        self.assertEqual(updated_data_obj.date.date(), datetime.now().date())
        self.assertEqual(updated_data_obj.creator, self.user)
        self.assertEqual(updated_data_obj.test_project_group, self.test_project_group)

    def test_write_data_with_not_latest_date(self):
        pass

class TestUpdate(TestCase):
    def setUp(self):
        self.manager = GeneralManager.__new__(GeneralManager)
        self.manager.group_model = TestProjectGroup
        self.manager.data_model = TestProject

        self.user = User.objects.create(microsoft_id= 'a')
        self.test_project_group = TestProjectGroup.objects.create()
        self.test_project = TestProject.objects.create(
             name='TestProject1',
             project_number='123456',
             test_project_group=self.test_project_group,
             date=datetime(2023, 5, 15),
             creator = self.user
        )
        self.manager.group_id = self.test_project_group.id
        self.manager._GeneralManager__group_obj = self.test_project_group
        self.manager._GeneralManager__group_model_name = 'test_project_group'
        self.manager.id = self.test_project.id
        self.creator_user_id = self.user.id

    def test_update(self):
        project_number_updated = '1234567890'

        self.manager.update(creator_user_id=self.creator_user_id, project_number= project_number_updated)
        updated_data_obj = TestProject.objects.latest('id')
        self.assertEqual(updated_data_obj.project_number, '1234567890')

        
    def test_update_with_multiple_kwargs(self):
        project_number_updated = '1234567890'
        name_updated = 'TestProject1Updated'        

        self.manager.update(creator_user_id=self.creator_user_id, project_number= project_number_updated, name=name_updated)
        updated_data_obj = TestProject.objects.latest('id')
        self.assertEqual(updated_data_obj.project_number, '1234567890') 
        self.assertEqual(updated_data_obj.name, 'TestProject1Updated')

    def test_update_changing_date(self):
        date_updated = datetime.now()
        with self.assertRaises(ValueError):
           self.manager.update(creator_user_id=self.creator_user_id, date = date_updated)
        
    def test_update_changing_group_id(self):
        new_group = TestProjectGroup.objects.create()
        group_updated = new_group.id
        with self.assertRaises(ValueError):
           self.manager.update(creator_user_id=self.creator_user_id, group_id = group_updated )

class TestDeactivate(TestCase):
    def setUp(self):
        self.manager = GeneralManager.__new__(GeneralManager)
        GeneralManager.group_model = TestProjectGroup
        GeneralManager.data_model = TestProject2

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
        self.creator_user_id = self.user.id
        self.manager.group_id = self.test_project_group.id
        self.manager._GeneralManager__group_obj = self.test_project_group
        self.manager._GeneralManager__group_model_name = 'test_project_group'
        self.manager.id = self.test_project.id
        self.manager.active = self.test_project.active

    def test_deactivate(self):
        self.assertTrue(self.test_project.active)
        self.manager.deactivate(creator_user_id=self.creator_user_id)
        deactivated_data_obj = TestProject2.objects.latest('id')
        self.assertFalse(deactivated_data_obj.active)

    def test_deactivate_twice(self):
        self.manager.deactivate(creator_user_id=self.creator_user_id)
        with self.assertRaises(NotUpdatableError):
            self.manager.deactivate(creator_user_id=self.creator_user_id)

class TestCreate(TestCase):
    def setUp(self):
        self.manager = GeneralManager.__new__(GeneralManager)
        GeneralManager.group_model = TestProjectGroup2
        GeneralManager.data_model = TestProject3

        self.user = User.objects.create(microsoft_id= 'a')
        self.test_project_group = TestProjectGroup2.objects.create(
            unique1 = 'a',
            unique2 = 'a'
        )
        self.test_project = TestProject3.objects.create(
             name='TestProject1',
             project_number='123',
             test_project_group2=self.test_project_group,
             date=datetime(2023, 5, 15),
             creator = self.user,
             active = True
        )
        self.creator_user_id = self.user.id

        self.test_project_user_group2 = TestProjectUserGroup2.objects.create(
            unique1ProjectUserGroup = 'a',
            unique2ProjectUserGroup = 'a'
        )
        self.test_project_user_role1 = TestProjectUserRole.objects.create(role_name='Role 1')
        self.test_project_user_role2 = TestProjectUserRole.objects.create(role_name='Role 2')
        

    def test_create_new(self):
        creator_user_id = self.creator_user_id
        group_data = {
            "unique1": 'a',
            "unique2": 'b'
        }
        data_data = {
            'name': 'TestProjectNew',
            'project_number': '123456New',
            'ap_no': None
        }
    
        def dummy_init(self, group_id, search_date=None):
            self.group_id = group_id
            self.active = 1
            self.date = datetime.now()
            self.search_date = search_date
        with patch.object(GeneralManager, '__init__', new = dummy_init):
            self.manager.create(creator_user_id, **group_data, **data_data)

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
        creator_user_id = self.creator_user_id
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
            self.date = datetime.now()
            self.search_date = search_date
        with patch.object(GeneralManager, '__init__', new = dummy_init):
            self.manager.create(creator_user_id, **group_data, **data_data)

            group_entries = TestProjectGroup2.objects.count()
            data_entries = TestProject3.objects.count()
            self.assertEqual(group_entries,1)
            self.assertEqual(data_entries,2)

            created_data = TestProject3.objects.latest('id')
            self.assertEqual(created_data.name, 'TestProjectNew')
            self.assertEqual(created_data.project_number, '123456New')
            self.assertEqual(created_data.test_project_group2, self.test_project_group)
            self.assertTrue(created_data.active)

    def test_create_many_to_many_relation_with_existing_group_id(self):
        
        self.manager = GeneralManager.__new__(GeneralManager)
        GeneralManager.group_model = TestProjectUserGroup2
        GeneralManager.data_model = TestProjectUser2

        creator_user_id = self.creator_user_id
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
            self.date = datetime.now()
            self.search_date = search_date

        with patch.object(GeneralManager, '__init__', new = dummy_init):
            self.manager.create(creator_user_id, **group_data, **data_data)

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
        creator_user_id = self.creator_user_id

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
            self.date = datetime.now()
            self.search_date = search_date

        with patch.object(GeneralManager, '__init__', new = dummy_init):
            self.manager.create(creator_user_id, **group_data, **data_data)

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
        creator_user_id = self.creator_user_id
        group_data = {
            "unique1": 'a',   
            "unique2": 'a'
        }
        data_data = {
            'name': 'TestProjectNew',
            'project_number': '123456New',
            'ap_no': None,
            'test_project_group' : self.test_project_group
        }

        with self.assertRaises(ValueError): 
            self.manager.create(creator_user_id, **group_data, **data_data)   
    
      
    