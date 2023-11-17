import unittest
from backend.src.auxiliary.list_of_dicts import groupListOfDictsByListOfStrings

class TestGroupListOfDictsByListOfStrings(unittest.TestCase):
    def test_validGrouping(self):
        data = [
            {"name": "John", "age": 30, "city": "New York"},
            {"name": "Jane", "age": 25, "city": "New York"},
            {"name": "John", "age": 40, "city": "Los Angeles"},
        ]
        group_by = ["name"]
        result = groupListOfDictsByListOfStrings(data, group_by)
        expected_result_1 = [
            {"name": "John", "age": 70, "city": "Los Angeles, New York"},
            {"name": "Jane", "age": 25, "city": "New York"},
        ]
        expected_result_2 = [
            {"name": "John", "age": 70, "city": "New York, Los Angeles"},
            {"name": "Jane", "age": 25, "city": "New York"},
        ]
        print('result', result)
        self.assertEqual(result, any(expected_result_1,expected_result_2))

    def test_invalidGroupBy(self):
        data = [
            {"name": "John", "age": 30, "city": "New York"},
            {"name": "Jane", "age": 25, "city": "New York"},
            {"name": "John", "age": 40, "city": "Los Angeles"},
        ]
        group_by = ["invalid_key"]
        with self.assertRaises(Exception):
            groupListOfDictsByListOfStrings(data, group_by)

    def test_checkGroupByFormat(self):
        group_by_list = ["name.age"]
        result_list_of_dict = [{"name": {"age": 30}}, {"name": {"age": 25}}]
        self.assertIsNone(groupListOfDictsByListOfStrings(group_by_list, result_list_of_dict))

        group_by_list = ["name.age", "name.city"]
        with self.assertRaises(Exception):
            groupListOfDictsByListOfStrings(group_by_list, result_list_of_dict)

        group_by_list = ["name"]
        with self.assertRaises(Exception):
            groupListOfDictsByListOfStrings(group_by_list, result_list_of_dict)

    def test_getGroupLevelDict(self):
        group_by_list = ["name.age", "city"]
        level_1_list, level_2_dict = groupListOfDictsByListOfStrings(group_by_list)
        self.assertEqual(level_1_list, ["city"])
        self.assertEqual(level_2_dict, {"name": ["age"]})

if __name__ == '__main__':
    unittest.main()