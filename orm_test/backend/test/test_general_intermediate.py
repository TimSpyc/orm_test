from datetime import datetime
from backend.src.auxiliary.manager import GeneralManager
from backend.src.auxiliary.intermediate import GeneralIntermediate
from backend.test.models_for_testing import TestProject, TestProjectGroup
from django.test import TestCase



class TestGetStartDate(TestCase):
    def setUp(self):

        self.manager.group_id = 1
        self.search_date = datetime(2023, 7, 28)
        self.scenario_dict = {'scenario_key': 'scenario_value'}
        self.dependencies = [self.manager]   


        self.intermediate = GeneralIntermediate(
            search_date=self.search_date,
            scenario_dict=self.scenario_dict,
            dependencies=self.dependencies,
        )
        self.intermediate.relevant_scenario_keys = [('volume', 'project')]


    def test_get_start_date(self):
        
        # Test getting the start date when all dependencies have valid start dates
        start_date = self.intermediate.__getStartDate()
        self.assertEqual(start_date, datetime(2023, 7, 28))

        # Test getting the start date when some dependencies have None start dates
        self.intermediate.dependencies[0].start_date = None
        start_date = self.intermediate.__getStartDate()
        self.assertEqual(start_date, datetime(2023, 7, 28))

        # Test getting the start date when all dependencies have None start dates
        for dependency in self.intermediate.dependencies:
            dependency.start_date = None
        start_date = self.intermediate.__getStartDate()
        self.assertIsNone(start_date)



# class TestGetEndDate(TestCase):
#     def setUp(self):
#         self.search_date = datetime(2023, 7, 28)
#         self.scenario_dict = {'scenario_key': 'scenario_value'}
#         self.dependencies = [GeneralManager(), GeneralIntermediate()]

#     def test_get_end_date(self):
#         intermediate = GeneralIntermediate(
#             search_date=self.search_date,
#             scenario_dict=self.scenario_dict,
#             dependencies=self.dependencies
#         )
#         # Test getting the end date when all dependencies have valid end dates
#         end_date = intermediate.__getEndDate()
#         self.assertEqual(end_date, datetime(2023, 7, 28))

#         # Test getting the end date when some dependencies have None end dates
#         intermediate.dependencies[0].end_date = None
#         end_date = intermediate.__getEndDate()
#         self.assertEqual(end_date, datetime(2023, 7, 28))

#         # Test getting the end date when all dependencies have None end dates
#         for dependency in intermediate.dependencies:
#             dependency.end_date = None
#         end_date = intermediate.__getEndDate()
#         self.assertIsNone(end_date)



# class TestCheckIfDependenciesAreFilled(TestCase):

# class TestMakeArgsToKwargs(TestCase):
    
# class TestCleanScenarioDict(TestCase):

# class TestupdateCache(TestCase):