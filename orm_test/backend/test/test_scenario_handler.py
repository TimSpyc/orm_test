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
        result = ScenarioHandler._ScenarioHandler__addValuesToDict(key_chain, scenario_dict, {})
        self.assertEqual(result, scenario_dict)

    def test_single_value_length_2(self):
        scenario_dict = {
            'test': 123,
            'hallo': 123,
        }
        key_chain = ['test',]
        result = ScenarioHandler._ScenarioHandler__addValuesToDict(key_chain, scenario_dict, {})
        self.assertEqual(result, {'test': 123,})

    # def test_single_value_length_3(self):
    #     scenario_dict = {
    #         'test': 123,
    #         'hallo': {'how': {'are': {'you': '?'}}},
    #     }
    #     key_chain = ['hallo', 'how']
    #     result = ScenarioHandler._ScenarioHandler__addValuesToDict(key_chain, scenario_dict, {})
    #     self.assertEqual(result, {'hallo': {'how': {'are': {'you': '?'}}}})
