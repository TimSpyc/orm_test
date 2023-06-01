from django.test import TestCase
from backend.src.auxiliary.manager import transferToSnakeCase, noneValueInNotNullField, updateCache

class TestTransferToSnakeCase(TestCase):
    
    def test_basic(self):
        self.assertEqual(transferToSnakeCase('CamelCase'), 'camel_case')

    def test_basic_longer(self):
        self.assertEqual(transferToSnakeCase('CamelCaseLonger'), 'camel_case_longer')    

    def test_single_word(self):
        self.assertEqual(transferToSnakeCase('Camel'), 'camel')

    def test_multiple_uppercase(self):
        self.assertEqual(transferToSnakeCase('HTTPRequest'), 'http_request')

    def test_all_uppercase(self):
        self.assertEqual(transferToSnakeCase('CAMELCASE'), 'camelcase')  

    def test_all_lowercase(self):
        self.assertEqual(transferToSnakeCase('camelcase'), 'camelcase')      

    def test_empty_string(self):
        self.assertEqual(transferToSnakeCase(""), "")



class TestNoneValueInNotNullField(TestCase):

    def test_no_none_value(self):
        not_null_fields = ['field1', 'field2']
        data_dict = {'field1': 'value1', 'field2': 'value2'}
        self.assertFalse(noneValueInNotNullField(not_null_fields, data_dict))

    def test_none_value_present(self):
        not_null_fields = ['field1', 'field2']
        data_dict = {'field1': None, 'field2': 'value2'}
        self.assertTrue(noneValueInNotNullField(not_null_fields, data_dict))

    def test_all_none_values(self):
        not_null_fields = ['field1', 'field2']
        data_dict = {'field1': None, 'field2': None}
        self.assertTrue(noneValueInNotNullField(not_null_fields, data_dict))

    def test_none_values_in_null_allowed_fields(self):
        not_null_fields = ['field1', 'field2']
        data_dict = {'field1': 'value1', 'field2': 'value2', 'field3': None}
        self.assertFalse(noneValueInNotNullField(not_null_fields, data_dict))

    def test_with_additional_fields(self):
        not_null_fields = ['field1', 'field2', 'field3']
        data_dict = {'field1': 'value1', 'field2': 'value2', 'field3': True, 'field4': None, 'field5': 'xyz'}
        self.assertFalse(noneValueInNotNullField(not_null_fields, data_dict))   

    def test_with_empty_data_dict(self):
        not_null_fields = ['field1', 'field2']
        data_dict = {}
        self.assertFalse(noneValueInNotNullField(not_null_fields, data_dict))

class Cache:
    def __init__(self):
        self.cache = {}

    @updateCache
    def add_entry(self, key, value):
        self.cache[key] = value
        return True

    def updateCache(self):
        self.cache['updated'] = True


class TestCacheDecorators(TestCase):
    
    def test_update_cache(self):
        cache = Cache()
        cache.add_entry('key', 'value')
        self.assertTrue(cache.cache['updated'])
