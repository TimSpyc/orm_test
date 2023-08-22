from datetime import datetime, date
from json import JSONDecoder
import json
from backend.models.caching_models import CacheIntermediate, CacheManager
from backend.src.auxiliary.manager import GeneralManager
from backend.src.auxiliary.intermediate import GeneralIntermediate
from backend.src.auxiliary.scenario_handler import ScenarioHandler
from backend.test.models_for_testing import TestProject, TestProjectGroup
from django.test import TestCase
from unittest.mock import Mock, patch
from django.core.cache import cache


class TestGetStartDate(TestCase):
    def setUp(self):
        GeneralManager.group_model = TestProjectGroup
        GeneralManager.data_model = TestProject
        self.manager = GeneralManager.__new__(GeneralManager)
        self.manager.group_id = 1
        self.manager.start_date = datetime(2023, 7, 27)
        self.manager.end_date = None
        search_date=datetime(2023, 7, 28)

        self.manager._identification_dict = {
            'group_id': self.manager.group_id,
            'manager_name': self.manager.__class__.__name__,
            'start_date': self.manager.start_date,
            'end_date': self.manager.end_date
        }

        GeneralIntermediate.relevant_scenario_keys = []
        self.intermediate = object.__new__(GeneralIntermediate)
        
        scenario_dict={'scenario_key': 'scenario_value'},
        dependencies=[self.manager]
        self.intermediate._identification_dict = {
            'intermediate_name': 'test_intermediate',
            'kwargs': {'search_date': search_date}
        }
        self.intermediate.__init__(
            scenario_dict=scenario_dict,
            dependencies=dependencies,
            search_date=search_date
        )

    def test_get_start_date_with_valid_start_dates(self):
        start_date = self.intermediate._GeneralIntermediate__getStartDate()
        self.assertEqual(start_date, datetime(2023, 7, 27))

    ## darf startdate none sind,?
    # def test_get_start_date_with_manager_no_start_date(self):
    #     self.manager.start_date = None
    #     print('start_date',self.manager.start_date)

    #     start_date = self.intermediate._GeneralIntermediate__getStartDate()
    #     self.assertIsNone(start_date)


class TestGetEndDate(TestCase):
    def setUp(self):
        GeneralManager.group_model = TestProjectGroup
        GeneralManager.data_model = TestProject
        self.manager = GeneralManager.__new__(GeneralManager)
        self.manager.group_id = 1
        self.manager.start_date = datetime(2023, 7, 27)
        self.manager.end_date = datetime(2023, 7, 28)
        search_date=datetime(2023, 7, 28)

        self.manager._identification_dict = {
            'group_id': self.manager.group_id,
            'manager_name': self.manager.__class__.__name__,
            'start_date': self.manager.start_date,
            'end_date': self.manager.end_date
        }
        GeneralIntermediate.relevant_scenario_keys = []
        self.intermediate = object.__new__(GeneralIntermediate)
        
        scenario_dict={'scenario_key': 'scenario_value'},
        dependencies=[self.manager]
        self.intermediate._identification_dict = {
            'intermediate_name': 'test_intermediate',
            'kwargs': {'search_date': search_date}
        }
        self.intermediate.__init__(
            scenario_dict=scenario_dict,
            dependencies=dependencies,
            search_date=search_date
        )

    def test_get_end_date(self):
        end_date =  self.intermediate.end_date
        self.assertEqual(end_date, datetime(2023, 7, 28))

    # def test_get_start_date_with_none_end_dates(self):
    #     self.manager.end_date = None
    #     end_date = self.intermediate.end_date
    #     self.assertIsNone(end_date)



class TestCheckIfDependenciesAreFilled(TestCase):
    def setUp(self):
        GeneralManager.group_model = TestProjectGroup
        GeneralManager.data_model = TestProject
        self.manager = GeneralManager.__new__(GeneralManager)
        self.manager.group_id = 1
        self.manager.start_date = datetime(2023, 7, 27)
        self.manager.end_date = datetime(2023, 7, 28)
        self.search_date=datetime(2023, 7, 28)
        self.manager._identification_dict = {
            'group_id': self.manager.group_id,
            'manager_name': self.manager.__class__.__name__,
            'start_date': self.manager.start_date,
            'end_date': self.manager.end_date
        }
        GeneralIntermediate.relevant_scenario_keys = []
        

    def test_check_dependencies_with_valid_dependencies(self):
        intermediate = object.__new__(GeneralIntermediate) 
        scenario_dict={'scenario_key': 'scenario_value'},
        dependencies=[self.manager]
        intermediate._identification_dict = {
            'intermediate_name': 'test_intermediate',
            'kwargs': {'search_date': self.search_date}
        }
        intermediate.__init__(
            scenario_dict=scenario_dict,
            dependencies=dependencies,
            search_date=self.search_date
        )
        try:
            intermediate._GeneralIntermediate__checkIfDependenciesAreFilled()
        except Exception as e:
            self.fail(f'Eine Ausnahme wurde ausgelöst: {str(e)}')


            #####
    # def test_check_dependencies_without_dependencies(self):
    #     intermediate = object.__new__(GeneralIntermediate)
    #     scenario_dict={'scenario_key': 'scenario_value'},
    #     dependenciesEmpty=[]
    #     intermediate._identification_dict = {
    #         'intermediate_name': 'test_intermediate',
    #         'kwargs': {'search_date': self.search_date}
    #     }
    #     intermediate.__init__(
    #         scenario_dict=scenario_dict,
    #         dependencies=dependenciesEmpty,
    #         search_date=self.search_date
    #     )
    #     print('PRINT',  intermediate.__init__(
    #         scenario_dict=scenario_dict,
    #         dependencies=dependenciesEmpty,
    #         search_date=self.search_date
    #     ))
    #     with self.assertRaises(ValueError):
    #         intermediate._GeneralIntermediate__checkIfDependenciesAreFilled()

        
    # def test_check_dependencies_with_invalid_dependencies(self):
    #     self.intermediate = object.__new__(GeneralIntermediate)
    #     scenario_dict={'scenario_key': 'scenario_value'},
    #     self.invalid_dependency = ['invalid_dependency'] 
    #     self.intermediate._identification_dict = {
    #         'intermediate_name': 'test_intermediate',
    #         'kwargs': {'search_date': self.search_date}
    #     }
    #     self.intermediate.__init__(
    #         scenario_dict=scenario_dict,
    #         dependencies=self.invalid_dependency,
    #         search_date=self.search_date
    #     )
    #     with self.assertRaises(TypeError):
    #         self.intermediate._GeneralIntermediate__checkIfDependenciesAreFilled()



class TestMakeArgsToKwargs(TestCase):

    def test_make_args_to_kwargs(self):
        args = [1, 2, 3]
        kwargs = {'a': 'testA', 'b': 'TestB'}
        expected_result = {'a': 'testA', 'b': 'TestB', 'scenario_dict': 3, 'search_date': 2, 'self': 1}  

        result = GeneralIntermediate._GeneralIntermediate__makeArgsToKwargs(args, kwargs)
        self.assertEqual(result, expected_result)

    def test_make_args_to_kwargs_empty_args_list(self):
        args = []
        kwargs = {'a': 'testA', 'b': 'TestB'}
        expected_result = {'a': 'testA', 'b': 'TestB'}  

        result = GeneralIntermediate._GeneralIntermediate__makeArgsToKwargs(args, kwargs)
        self.assertEqual(result, expected_result)

    def test_make_args_to_kwargs_empty_kwargs_dic(self):
        args = [1,2,3]
        kwargs = {}
        expected_result = {'scenario_dict': 3, 'search_date': 2, 'self': 1}  

        result = GeneralIntermediate._GeneralIntermediate__makeArgsToKwargs(args, kwargs)
        self.assertEqual(result, expected_result)
    
    def test_make_args_to_kwargs_empty_kwargs_and_args(self):
        args = []
        kwargs = {}
        expected_result = {}  

        result = GeneralIntermediate._GeneralIntermediate__makeArgsToKwargs(args, kwargs)
        self.assertEqual(result, expected_result)
    

class TestCleanScenarioDict(TestCase):
    def setUp(self):
        GeneralManager.group_model = TestProjectGroup
        GeneralManager.data_model = TestProject
        self.manager = GeneralManager.__new__(GeneralManager)
        self.manager.group_id = 1
        self.manager.start_date = datetime(2023, 7, 27)
        self.manager.end_date = datetime(2023, 7, 28)
        self.search_date=datetime(2023, 7, 28)
        self.manager._identification_dict = {
            'group_id': self.manager.group_id,
            'manager_name': self.manager.__class__.__name__,
            'start_date': self.manager.start_date,
            'end_date': self.manager.end_date
        }
        GeneralIntermediate.relevant_scenario_keys = [('key1', 'key2')]

        self.intermediate = object.__new__(GeneralIntermediate)
        scenario_dict={'scenario_key': 'scenario_value'},
        dependencies=[self.manager]
        self.intermediate._identification_dict = {
            'intermediate_name': 'test_intermediate',
            'kwargs': {'search_date': self.search_date}
        }
        self.intermediate.__init__(
            scenario_dict=scenario_dict,
            dependencies=dependencies,
            search_date=self.search_date
        )

    def test_clean_scenario_dict(self):
        scenario_dict = {
            'key1': {'key2': 'value1'},
            'key3': 'value3',
            'keyA': 'test_keyA',
            'scenario_key': 'scenario_value'
        }
        cleaned_scenario, scenario_handler = self.intermediate._GeneralIntermediate__cleanScenarioDict(scenario_dict)

        self.assertIsInstance(scenario_handler, ScenarioHandler)
        self.assertEqual(cleaned_scenario, {'key1': {'key2': 'value1'}})

    def test_clean_scenario_dict_non_existing_keys(self):
        scenario_dict = {
            # 'key1': {'key2': 'value1'},
            'key3': 'value3',
            'keyA': 'test_keyA',
            'scenario_key': 'scenario_value'
        }
        cleaned_scenario, scenario_handler = self.intermediate._GeneralIntermediate__cleanScenarioDict(scenario_dict)

        self.assertIsInstance(scenario_handler, ScenarioHandler)
        self.assertEqual(cleaned_scenario, {})

    def test_clean_scenario_dict_with_empty_dict(self):
        scenario_dict = {
        }
        cleaned_scenario, scenario_handler = self.intermediate._GeneralIntermediate__cleanScenarioDict(scenario_dict)

        self.assertIsInstance(scenario_handler, ScenarioHandler)
        self.assertEqual(cleaned_scenario, {})

    def test_clean_scenario_dict_with_invalid_dict(self):
        scenario_dict = 'invalid_dict'
        cleaned_scenario, scenario_handler = self.intermediate._GeneralIntermediate__cleanScenarioDict(scenario_dict)

        self.assertIsInstance(scenario_handler, ScenarioHandler)
        self.assertEqual(cleaned_scenario, {})

        






    
class TestUpdateCache(TestCase):
    def setUp(self):
        GeneralManager.group_model = TestProjectGroup
        GeneralManager.data_model = TestProject
        self.manager = GeneralManager.__new__(GeneralManager)
        self.manager.group_id = 1
        self.manager.start_date = datetime(2023, 7, 27)
        self.manager.end_date = datetime(2023, 7, 28)
        self.search_date=datetime(2023, 7, 28)
        self.manager._identification_dict = {
            'group_id': self.manager.group_id,
            'manager_name': self.manager.__class__.__name__,
            'start_date': self.manager.start_date,
            'end_date': self.manager.end_date
        }
        GeneralIntermediate.relevant_scenario_keys = []
        self.intermediate = object.__new__(GeneralIntermediate) 
        scenario_dict={'scenario_key': 'scenario_value'},
        dependencies=[self.manager]
        self.intermediate._identification_dict = {
            'intermediate_name': 'test_intermediate',
            'kwargs': {'search_date': self.search_date}
        }
        self.intermediate.__init__(
            scenario_dict=scenario_dict,
            dependencies=dependencies,
            search_date=self.search_date
        )

    def test_update_cache(self):
        cache.clear()
        self.intermediate.updateCache()
        id_string = CacheIntermediate.getIdString(self.intermediate._identification_dict)
        print('id_string', id_string)
        cached_data = cache.get(id_string)
        print('cached_data', cached_data)
        self.assertIsNotNone(cached_data)
        self.assertEqual(cached_data, self.intermediate)  
        
            





    # def test_update_cache_with_end_date_none(self):
    #     #start_date = datetime(year=2023, month=8, day=22)
    #     self.intermediate.updateCache()
    #     id_string = CacheIntermediate.getIdString(self.intermediate._identification_dict)
    #     cached_data = cache.get(id_string)
        
    #     self.assertIsNotNone(cached_data)
    #     self.assertEqual(cached_data, self.intermediate)

    # def test_update_cache_with_end_date_set(self):
    #     """
    #     Test updating the cache when the end date is set.
    #     """
    #     identification_dict = {'test_key': 'test_value'}
    #     start_date = datetime(2023, 7, 1)
    #     end_date = datetime(2023, 7, 5)
    #     intermediate = GeneralIntermediate(None, identification_dict, start_date, end_date)
        
    #     intermediate.updateCache()
        
    #     id_string = CacheIntermediate.getIdString(identification_dict)
    #     cached_data = cache.get(id_string)
        
    #     self.assertIsNotNone(cached_data)
    #     self.assertEqual(cached_data, intermediate)





    # def test_update_cache_custom_data(self):
    #     """
    #     Test updating the cache with custom data.
    #     """
    #     identification_dict = {'test_key': 'test_value'}
    #     start_date = datetime(2023, 7, 1)
    #     end_date = datetime(2023, 7, 5)
    #     custom_data = {'custom_key': 'custom_value'}
    #     intermediate = GeneralIntermediate(None, identification_dict, start_date, end_date)
        
    #     intermediate.updateCache(custom_data)
        
    #     id_string = CacheIntermediate.getIdString(identification_dict)
    #     cached_data = cache.get(id_string)
        
    #     self.assertIsNotNone(cached_data)
    #     self.assertEqual(cached_data, custom_data)





# class TestCheckIfCacheNeedsToExpire(TestCase):


# class TestExpireCache(TestCase):