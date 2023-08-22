from django.test import TestCase
from backend.src.auxiliary.scenario_handler import ScenarioHandler


class TestCheckIfScenarioDictIsFilled(TestCase):

    def test_valid_easy(self):
        relevant_scenario_keys = [('and',)]
        ScenarioHandler._ScenarioHandler__checkIfRelevantScenarioKeysIsFilled(relevant_scenario_keys)

    def test_valid_complex(self):
        relevant_scenario_keys = [('test', 'this', 'function'), ('and',), ('test', 'this', 'good')]
        ScenarioHandler._ScenarioHandler__checkIfRelevantScenarioKeysIsFilled(relevant_scenario_keys)

    def test_not_type_list(self):
        relevant_scenario_keys = ('and',)
        with self.assertRaises(TypeError):
            ScenarioHandler._ScenarioHandler__checkIfRelevantScenarioKeysIsFilled(relevant_scenario_keys)

    def test_not_type_tuple_list(self):
        relevant_scenario_keys = ['and', 1]
        with self.assertRaises(TypeError):
            ScenarioHandler._ScenarioHandler__checkIfRelevantScenarioKeysIsFilled(relevant_scenario_keys)

    def test_mixed_types(self):
        relevant_scenario_keys = [('test', 'this', 'function'), {'and'}, [('test', 'this', 'good')]]
        with self.assertRaises(TypeError):
            ScenarioHandler._ScenarioHandler__checkIfRelevantScenarioKeysIsFilled(relevant_scenario_keys)

class TestIsKeyChainInDict(TestCase):

    def test_key_chain_in_dict_1(self):
        scenario_dict = {
            'test': 3
        }
        key_chain = ('test',)
        result = ScenarioHandler._ScenarioHandler__isKeyChainInDict(scenario_dict, key_chain)
        self.assertTrue(result)

    def test_key_chain_in_dict_2(self):
        scenario_dict = {
            'test': {'this': {'function': {'id': 1, 'name': 2}}}
        }
        key_chain = ('test', 'this', 'function')
        result = ScenarioHandler._ScenarioHandler__isKeyChainInDict(scenario_dict, key_chain)
        self.assertTrue(result)

    def test_key_chain_in_dict_3(self):
        scenario_dict = {
            'test': {'this': 1}
        }
        key_chain = ('test', 'this')
        result = ScenarioHandler._ScenarioHandler__isKeyChainInDict(scenario_dict, key_chain)
        self.assertTrue(result)

    def test_key_chain_not_in_dict_1(self):
        scenario_dict = {
            'test': 123
        }
        key_chain = ('not in dict')
        result = ScenarioHandler._ScenarioHandler__isKeyChainInDict(scenario_dict, key_chain)
        self.assertFalse(result)

    def test_key_chain_not_in_dict_2(self):
        scenario_dict = {
            'test': {'this': {'function': {'id': 1, 'name': 2}}}
        }
        key_chain = ('test', 'not', 'in', 'dict')
        result = ScenarioHandler._ScenarioHandler__isKeyChainInDict(scenario_dict, key_chain)
        self.assertFalse(result)

    def test_key_chain_not_in_dict_2(self):
        scenario_dict = {
            'test': 123
        }
        key_chain = ('test', 'not', 'in', 'dict')
        result = ScenarioHandler._ScenarioHandler__isKeyChainInDict(scenario_dict, key_chain)
        self.assertFalse(result)

class TestAddValuesToDict(TestCase):

    def test_single_value_length_1(self):
        scenario_dict = {
            'test': 123
        }
        key_chain = ['test',]
        result = ScenarioHandler._ScenarioHandler__addValuesToDict(key_chain, scenario_dict)
        self.assertEqual(result, scenario_dict)

    def test_single_value_length_2(self):
        scenario_dict = {
            'test': 123,
            'hallo': 123,
        }
        key_chain = ['test',]
        result = ScenarioHandler._ScenarioHandler__addValuesToDict(key_chain, scenario_dict)
        self.assertEqual(result, {'test': 123,})

    def test_single_value_length_3(self):
        scenario_dict = {
            'test': 123,
            'hallo': {'how': {'are': {'you': '?'}}},
        }
        key_chain = ['hallo', 'how']
        result = ScenarioHandler._ScenarioHandler__addValuesToDict(key_chain, scenario_dict)
        self.assertEqual(result, {'hallo': {'how': {'are': {'you': '?'}}}})

class TestCheckIfRelevantScenarioKeysIsFilled(TestCase):

    def test_non_list_or_tuple(self):
        with self.assertRaises(TypeError) as context:
            ScenarioHandler._ScenarioHandler__checkIfRelevantScenarioKeysIsFilled("Dies ist keine Liste oder kein Tupel")
        
    def test_empty_list(self):
        try:
            ScenarioHandler._ScenarioHandler__checkIfRelevantScenarioKeysIsFilled([])
        except TypeError:
            print("Error: Empty list not accepted.")

    def test_list_and_tuple(self):
        try:
            ScenarioHandler._ScenarioHandler__checkIfRelevantScenarioKeysIsFilled([("key1", "key2"), ("key3",)])
        except TypeError:
            print("Testfall fehlgeschlagen: Liste und Tupel nicht akzeptiert.")

class TestMergeTwoDicts(TestCase):
    
    def test_merge_two_dicts_normal_case(self):
        dict1 = {'a': 1, 'b': 2}
        dict2 = {'c': 3, 'd': 4}
        merged_dict = ScenarioHandler._ScenarioHandler__mergeTwoDicts(dict1, dict2)
        self.assertEqual(merged_dict, {'a': 1, 'b': 2, 'c': 3, 'd': 4})

    def test_merge_two_dicts_conflict_case(self):
        dict1 = {'a': 1, 'b': 2}
        dict2 = {'b': 3, 'c': 4}
        try:
            merged_dict = ScenarioHandler._ScenarioHandler__mergeTwoDicts(dict1, dict2)
        except Exception as e:
            assert str(e) == 'Conflict at b'

    def test_merge_two_dicts_nested_case(self):
        dict1 = {'a': {'x': 1, 'y': 2}, 'b': {'z': 3}}
        dict2 = {'a': {'x': 1, 'z': 4}, 'c': {'w': 5}}
        merged_dict = ScenarioHandler._ScenarioHandler__mergeTwoDicts(dict1, dict2)
        self.assertEqual(merged_dict, {'a': {'x': 1, 'y': 2, 'z': 4}, 'b': {'z': 3}, 'c': {'w': 5}})

class TestGetRelevantScenarioDict(TestCase):
    def test_get_relevant_scenario_dict_single_keys(self):
        scenario_dict = {
            'user': {
                'name': 'John',
                'age': 30
            },
            'product': {
                'name': 'product1',
                'price': 20.0
            },
            'location': 'New York'
        }
        handler = ScenarioHandler(scenario_dict)
        relevant_scenario_keys = [('user', 'name'), ('product', 'price')]
        relevant_scenario = handler.getRelevantScenarioDict(relevant_scenario_keys)
        expected_result = {
            'user': {
                'name': 'John'
            },
            'product': {
                'price': 20.0
            }
        }
        self.assertEqual(relevant_scenario, expected_result)

    def test_get_relevant_scenario_dict_empty_keys(self):
        scenario_dict = {
            'user': {
                'name': 'John',
                'age': 30
            },
            'product': {
                'name': 'product1',
                'price': 20.0
            },
            'location': 'New York'
        }
        handler = ScenarioHandler(scenario_dict)
        relevant_scenario_keys = []
        relevant_scenario = handler.getRelevantScenarioDict(relevant_scenario_keys)
        expected_result = {}
        self.assertEqual(relevant_scenario, expected_result)


    def test_get_relevant_scenario_dict_nonexistent_keys(self):
        scenario_dict = {
            'user': {
                'name': 'John',
                'age': 30
            },
            'product': {
                'name': 'product1',
                'price': 20.0
            },
            'location': 'New York'
        }
        handler = ScenarioHandler(scenario_dict)
        relevant_scenario_keys = [('company', 'name'), ('location', 'city')]
        relevant_scenario = handler.getRelevantScenarioDict(relevant_scenario_keys)
        expected_result = {}
        self.assertEqual(relevant_scenario, expected_result)

    def test_get_relevant_scenario_dict_nested_keys(self):
        scenario_dict = {
            'user': {
                'profile': {
                    'name': 'John',
                    'age': 30
                },
            },
            'product': {
                'info': {
                    'name': 'product1',
                    'price': 20.0
                },
            },
            'location': 'New York'
        }
        handler = ScenarioHandler(scenario_dict)
        relevant_scenario_keys = [('user', 'profile', 'name',), ('product','info','price')]
        relevant_scenario = handler.getRelevantScenarioDict(relevant_scenario_keys)
        expected_result = {
            'user': {
                'profile': {
                    'name': 'John',
                },
            },
            'product': {
                'info': {
                    'price': 20.0,
                },
            },
        }
        self.assertEqual(relevant_scenario, expected_result)

    def test_get_relevant_scenario_dict_nested_keys_nonexistent(self):
        scenario_dict = {
            'user': {
                'profile': {
                    'name': 'John',
                    'age': 30
                },
            },
            'product': {
                'info': {
                    'name': 'product1',
                    'price': 20.0
                },
            },
            'location': 'New York'
        }
        handler = ScenarioHandler(scenario_dict)
        relevant_scenario_keys = [('user', 'profile', 'nonExistensKey',), ('product','info','price')]
        relevant_scenario = handler.getRelevantScenarioDict(relevant_scenario_keys)
        expected_result = {
            'product': {
                'info': {
                    'price': 20.0,
                },
            },
        }
        self.assertEqual(relevant_scenario, expected_result)

class TestIsKeyChainInDict(TestCase):
    def test_is_key_chain_in_dict_key_exists(self):
        scenario_dict = {
            'user': {
                'profile': {
                    'name': 'John',
                    'age': 30
                },
            },
            'product': {
                'info': {
                    'name': 'product1',
                    'price': 20.0
                },
            },
            'location': 'New York'
        }
        key_chain = ('user', 'profile', 'name')
        result = ScenarioHandler._ScenarioHandler__isKeyChainInDict(scenario_dict, key_chain)
        self.assertTrue(result)

    def test_is_key_chain_in_dict_key_not_exists(self):
        scenario_dict = {
            'user': {
                'profile': {
                    'name': 'John',
                    'age': 30
                },
            },
            'product': {
                'info': {
                    'name': 'product1',
                    'price': 20.0
                },
            },
            'location': 'New York'
        }
        key_chain = ('user', 'profile', 'email')
        result = ScenarioHandler._ScenarioHandler__isKeyChainInDict(scenario_dict, key_chain)
        self.assertFalse(result)

    def test_is_key_chain_in_dict_empty_key_chain(self):
        scenario_dict = {
            'user': {
                'profile': {
                    'name': 'John',
                    'age': 30
                },
            },
            'product': {
                'info': {
                    'name': 'product1',
                    'price': 20.0
                },
            },
            'location': 'New York'
        }
        key_chain = ()
        result = ScenarioHandler._ScenarioHandler__isKeyChainInDict(scenario_dict, key_chain)
        self.assertTrue(result)

    def test_is_key_chain_in_dict_invalid_dict(self):
        invalid_dict = {'name': 'John'}
        key_chain = ('user', 'profile', 'name')
        result = ScenarioHandler._ScenarioHandler__isKeyChainInDict(invalid_dict, key_chain)
        self.assertFalse(result)









    

