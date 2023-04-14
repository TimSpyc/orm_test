from django.test import TestCase
from your_module import transferToSnakeCase, noneValueInNotNullField, updateCache, createCache

class TestTransferToSnakeCase(TestCase):
    
    def test_basic(self):
        self.assertEqual(transferToSnakeCase('CamelCase'), 'camel_case')

    def test_single_word(self):
        self.assertEqual(transferToSnakeCase('Camel'), 'camel')

    def test_multiple_uppercase(self):
        self.assertEqual(transferToSnakeCase('HTTPRequest'), 'http_request')


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