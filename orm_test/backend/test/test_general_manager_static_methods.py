from unittest.mock import MagicMock, Mock
from backend.src.auxiliary.exceptions import NonExistentGroupError, NotUpdatableError, NotValidIdError
from django.test import TestCase
from backend.src.auxiliary.manager import GeneralManager
from datetime import date, datetime
from .models_for_testing import TestProject2, TestProjectGroup, TestProject, TestProjectUserGroup, TestProjectUserRole, TestProjectUser, TestUser
from backend.models import User
from django.core.exceptions import FieldDoesNotExist

from backend.src.auxiliary.manager import transferToSnakeCase


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

class TestCheckInputDictForCreation(TestCase):
   
   @classmethod
   def setUpTestData(self):
        project_group = TestProjectGroup.objects.create()
        TestProject.objects.create(
            name='TestProject1',
            project_number='123456',
            test_project_group = project_group
        )
        self.manager = GeneralManager.__new__(GeneralManager)
        self.manager.group_model = TestProjectGroup
        self.manager.data_model = TestProject


   def test_check_input_dict_for_creation(self):
        db_column = "id"
        value = 1 
        available_column_list = ['id','name', 'project_number', 'test_project_group']
        result = self.manager._GeneralManager__checkInputDictForCreation(db_column, value, available_column_list)
        self.assertEqual = (result, (db_column,value))
        
   def test_invalid_column(self):
    
        db_column = 'non_existent_column'
        value = 'Test'
        available_column_list = [c.name for c in TestProject._meta.get_fields()]
        #available_column_list2 = ['id', 'name', 'project_number', 'project_group'] #[c.name for c in TestProject.._meta.get_fields()]
        with self.assertRaises(ValueError):
           value = self.manager._GeneralManager__checkInputDictForCreation(db_column, value, available_column_list)         

   def test_not_valid_value_no_referencingModel_no_ManyToMany(self): #value wird nicht überschrieben bleibt so deswegen test passes
        db_column = "id"
        value = 2 
        available_column_list = ['id','name', 'project_number', 'test_project_group']
      
        result = self.manager._GeneralManager__checkInputDictForCreation(db_column, value, available_column_list)
        self.assertEqual = (result, (db_column,value))

   def test_value_is_referencingModel_with_not_valid_value(self):
        db_column = "test_project_group_id" #_id zeigt dass isReferencingModel
        value = 2 
        available_column_list = ['id','name', 'project_number', 'test_project_group']
        with self.assertRaises(NotValidIdError):
            value = self.manager._GeneralManager__checkInputDictForCreation(db_column, value, available_column_list)

   def test_value_is_ManyToMany_with_not_valid_value(self):
        db_column = "test_project_group_id_list" #_id_list zeigt dass isManyToMany
        value = [2] 
        available_column_list = ['id','name', 'project_number', 'test_project_group']
        with self.assertRaises(NotValidIdError):
            value = self.manager._GeneralManager__checkInputDictForCreation(db_column, value, available_column_list)


class TestCheckInputDictForUpdate(TestCase):
 
   @classmethod
   def setUpTestData(self):
        self.manager = GeneralManager.__new__(GeneralManager)
        self.manager.group_model = TestProjectGroup
        self.manager.data_model = TestProject

        project_group = TestProjectGroup.objects.create()
        TestProject.objects.create(
            name='TestProject1',
            project_number='123456',
            test_project_group = project_group,
            date= date.today()
        )
        self.manager._GeneralManager__group_model_name = project_group
    

   def test_valid_update(self):
        available_column_list = ['id', 'name', 'project_number', 'test_project_group']
        db_column = 'name'
        value = 'new Name'

        result = self.manager._GeneralManager__checkInputDictForUpdate(db_column, value, available_column_list)
        self.assertEqual(result, (db_column, value))

   def test_invalid_update_date(self):
        available_column_list = ['id', 'name', 'project_number', 'test_project_group','date', 'creator_user_id']
        db_column = 'date'
        value = '2023-04-04'
        with self.assertRaises(ValueError):
            value = self.manager._GeneralManager__checkInputDictForUpdate(db_column, value, available_column_list)


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


class TestProjectManager(GeneralManager):
    group_model = TestProjectGroup
    data_model = TestProject

    def __init__(self, test_project_group_id, search_date=None):
        group, data = super().__init__(
            group_id=test_project_group_id,
            search_date=search_date
            )

            
class TestFilter(TestCase):
    def setUp(self):

        self.test_project_group = TestProjectGroup.objects.create()
        self.user = User.objects.create()
        
        self.test_project = TestProject.objects.create(
            name='TestProject1',
            project_number='123456',
            test_project_group = self.test_project_group,
            date = date(2023, 5, 15),
            creator = self.user,
            active = True
        )
        self.manager = TestProjectManager(test_project_group_id = self.test_project_group.id)
    
    def test_filter_with_search_date(self):
        search_date = date(2023, 5, 16)
        result = self.manager.filter(search_date=search_date)

        expected_result = [
            #{'test_project_group_id': self.test_project_group.id, 'search_date': search_date},
            TestProjectManager(test_project_group_id= self.test_project_group.id, search_date= search_date)
        ]
 
        self.assertEqual(result, expected_result)





# class TestAll(TestCase):
#     def setUp(self):
#        GeneralManager.group_model = TestProjectGroup
#        GeneralManager.data_model = TestProject
#        self.manager = GeneralManager.__new__(GeneralManager)

#     def test_all_function(self):
#         project_group = TestProjectGroup.objects.create()
#         data1 = TestProject.objects.create(name='TestProject1',project_number='123',test_project_group = project_group)
#         data2 = TestProject.objects.create(name='TestProject2',project_number='123456',test_project_group = project_group)
#         data3 = TestProject.objects.create(name='TestProject3',project_number='123456789',test_project_group = project_group)

#         all_data = self.manager.all()
#         self.assertEqual(len(all_data), 3)

    # def test_all_filter_searchDate(self):   
    #     project_group = TestProjectGroup.objects.create()
    #     data1 = TestProject.objects.create(name='TestProject1',project_number='123',test_project_group = project_group, date=date(2023, 4, 4))
    #     data2 = TestProject.objects.create(name='TestProject2',project_number='123456',test_project_group = project_group, date=date(2023, 4, 5))
    #     data3 = TestProject.objects.create(name='TestProject3',project_number='123456789',test_project_group = project_group, date=date(2023, 4, 6))
        
    #     all_data = self.manager.all(date(2023,4,6))
    #     self.assertEqual(len(all_data), 1)




class TestGetDataForGroupAndDataTableByKwargs(TestCase):
    def setUp(self):
        self.manager = GeneralManager.__new__(GeneralManager)
        self.manager.group_model = TestProjectGroup
        self.manager.data_model = TestProject

        self.data_model_column_list = ['name', 'project_number','test_project_group']
        self.group_model_column_list = ['id']
    

    def test_get_data_for_group_and_data_table_by_kwargs(self):
        group_data_dict, data_data_dict = self.manager._GeneralManager__getDataForGroupAndDataTableByKwargs(   
            self.manager,
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
                self.manager,
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
                self.manager,
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
                        date=date(2023, 5, 13))
        test_project2 = TestProject.objects.create(
                        name='TestProject1',
                        project_number='123456',
                        test_project_group = project_group1,
                        date=date(2023, 4, 5))

        data_search_dict = {'name': 'TestProject1', 'project_number': '1234567'} 
        group_search_dict = {'id':1} 
        search_date = date(2023, 5, 16)

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
                        date=date(2022, 5, 15))
        
        test_project2 = TestProject.objects.create(
                        name='TestProject1',
                        project_number='1234567',
                        test_project_group = project_group1,
                        date=date(2023, 4, 5))
        data_search_dict = {} 
        group_search_dict = {} 
        search_date = date(2023, 5, 16)

        result = self.manager._GeneralManager__getFilteredManagerList(data_search_dict, group_search_dict, search_date)
        expected_result = [
            {'test_project_group_id': project_group1.id, 'search_date': search_date}
        ]
        self.assertEqual(result, expected_result)

    def test_with_empty_dicts_and_no_search_date(self):
            #get all instances if there is no filter criteria
            project_group1 = TestProjectGroup.objects.create()
            project_group2 = TestProjectGroup.objects.create()
            test_project1 = TestProject.objects.create(
                name='TestProject1',
                project_number='123456',
                test_project_group=project_group1,
                date=date(2022, 5, 15)
            )
            test_project2 = TestProject.objects.create(
                name='TestProject1',
                project_number='654321',
                test_project_group=project_group2,
                date=date(2023, 4, 5)
            )
            test_project3 = TestProject.objects.create(
            name='TestProject2',
            project_number='789012',
            test_project_group=project_group1,
            date=date(2023, 5, 16)
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
            date=date(2022, 5, 15)
        )
        test_project2 = TestProject.objects.create(
            name='TestProject1',
            project_number='1234567',
            test_project_group=project_group1,
            date=date(2023, 4, 5)
        )
 
        data_search_dict = {'name': 'TestProject2', 'project_number': '654321'}
        group_search_dict = {'id': 1}
        search_date = date(2023, 5, 16)
 
        result = self.manager._GeneralManager__getFilteredManagerList(data_search_dict, group_search_dict, search_date)
        expected_result = []
        self.assertEqual(result, expected_result)

    def test_get_filtered_manager_list__with_multiple_results(self):
        project_group1 = TestProjectGroup.objects.create()
        project_group2 = TestProjectGroup.objects.create()
        test_project1 = TestProject.objects.create(
            name='TestProject1',
            project_number='123456',
            test_project_group=project_group1,
            date=date(2022, 5, 15)
        )
        test_project2 = TestProject.objects.create(
            name='TestProject1',
            project_number='654321',
            test_project_group=project_group2,
            date=date(2023, 4, 5)
        )
        test_project3 = TestProject.objects.create(
            name='TestProject2',
            project_number='789012',
            test_project_group=project_group1,
            date=date(2023, 5, 16)
        )
 
        data_search_dict = {'name': 'TestProject1'}
        group_search_dict = {}
        search_date = date(2023, 5, 16)
 
        result = self.manager._GeneralManager__getFilteredManagerList(data_search_dict, group_search_dict, search_date)
        expected_result = [
            {'test_project_group_id': project_group1.id, 'search_date': search_date},
            {'test_project_group_id': project_group2.id, 'search_date': search_date}
        ]
        self.assertEqual(result, expected_result)

    def test_with_invalid_filters(self):
        project_group1 = TestProjectGroup.objects.create()
        test_project1 = TestProject.objects.create(
            name='TestProject1',
            project_number='123456',
            test_project_group=project_group1,
            date=date(2022, 5, 15)
        )
        data_search_dict = {'name': 'invalid_name'}
        group_search_dict = {'id': 2}
        search_date = date(2023, 5, 16)

        result = self.manager._GeneralManager__getFilteredManagerList(data_search_dict, group_search_dict, search_date)
        expected_result = []
        self.assertEqual(result, expected_result)

    # def test_with_search_date_equals_latest_date(self):
    #     project_group1 = TestProjectGroup.objects.create()
    #     test_project1 = TestProject.objects.create(
    #         name='TestProject2',
    #         project_number='123456',
    #         test_project_group=project_group1,
    #         date=date(2023, 5, 15)
    #     )
    #     test_project2 = TestProject.objects.create(
    #         name='TestProject1',
    #         project_number='654321',
    #         test_project_group=project_group1,
    #         date=date(2023, 4, 5)
    #     )

    #     data_search_dict = {'name': 'TestProject2'}
    #     group_search_dict = {}
    #     search_date = date(2023, 5, 15)

    #     result = self.manager._GeneralManager__getFilteredManagerList(data_search_dict, group_search_dict, search_date)

    #     expected_result = [
    #         {'test_project_group_id': project_group1.id, 'search_date': search_date},
    #     ]
    #     self.assertEqual(result, expected_result)   ##datum ist auf sekunde genau deswegen klappt nicht
       

class TestErrorIfNotUpdatable(TestCase):
    def setUp(self):

        self.manager = GeneralManager.__new__(GeneralManager) #group_id=self.model.test_project_group
        self.manager.group_model = TestProjectGroup
        self.manager.data_model = TestProject
        
        project_group1 = TestProjectGroup.objects.create()
        self.model = TestProject.objects.create(
            name='testproject1',
            project_number='1234567',
            test_project_group = project_group1, 
        )
        self.manager._GeneralManager__group_obj = project_group1
        
      
    def test_error_if_not_updatable_latest(self):
        self.manager.id = self.model.id
        self.manager._GeneralManager__errorIfNotUpdatable()

    def test_not_latest(self):
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
        GeneralManager.group_model = TestProjectGroup
        GeneralManager.data_model = TestProject
        self.manager = GeneralManager.__new__(GeneralManager)

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
            'date': date(2023, 5, 22),
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
            'date': date(2023, 5, 22),
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
            'date': date(2023, 5, 22),
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
            'date': date(2023, 5, 22),
            'test_project_group': 1
        }
        contains_all_unique_fields, contains_all_not_null_fields, all_not_null_fields_contain_data = self.manager._GeneralManager__isDataUploadable(data_dict, TestProject)
 
        self.assertTrue(contains_all_unique_fields)
        self.assertTrue(contains_all_not_null_fields)
        self.assertFalse(all_not_null_fields_contain_data)


class TestWriteDataData(TestCase):
    def setUp(self):
        self.manager = GeneralManager.__new__(GeneralManager) 
        self.manager.group_model = TestProjectGroup
        self.manager.data_model = TestProject

    def test_write_data_data(self):
        pass    