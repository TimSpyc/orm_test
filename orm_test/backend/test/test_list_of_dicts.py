import unittest
from backend.src.auxiliary.list_of_dicts import groupListOfDictsByListOfStrings

class TestGroupListOfDictsByListOfStrings(unittest.TestCase):
    def testGrouping(self):
        data = [
            {"name": "John", "age": 30, "city": "New York"},
            {"name": "Jane", "age": 25, "city": "New York"},
            {"name": "John", "age": 40, "city": "Los Angeles"},
        ]
        group_by = ["name"]
        result = groupListOfDictsByListOfStrings(data, group_by)
        expected_result = [
            {"name": "John", "age": 70, "city": "Los Angeles, New York"},
            {"name": "Jane", "age": 25, "city": "New York"},
        ]
        print('result', result)
        self.assertEqual(result, expected_result)

    def testInvalidGroupBy(self):
        data = [
            {"name": "John", "age": 30, "city": "New York"},
            {"name": "Jane", "age": 25, "city": "New York"},
            {"name": "John", "age": 40, "city": "Los Angeles"},
        ]
        group_by = ["invalid_key"]
        with self.assertRaises(Exception):
            groupListOfDictsByListOfStrings(data, group_by)

    # def testCheckGroupByFormat(self):
    #     group_by_list = ["name.age"]
    #     result_list_dict = [{"name": {"age": 30}}, {"name": {"age": 25}}]
    #     self.assertIsNone(groupListOfDictsByListOfStrings(group_by_list, result_list_dict))

    #     group_by_list = ["name.age", "name.city"]
    #     with self.assertRaises(Exception):
    #         groupListOfDictsByListOfStrings(group_by_list, result_list_dict)

    #     group_by_list = ["name"]
    #     with self.assertRaises(Exception):
    #         groupListOfDictsByListOfStrings(group_by_list, result_list_dict)

    # def testGetGroupLevelDict(self):
    #     group_by_list = ["name.age", "city"]
    #     level_1_list, level_2_dict = groupListOfDictsByListOfStrings(group_by_list)
    #     self.assertEqual(level_1_list, ["city"])
    #     self.assertEqual(level_2_dict, {"name": ["age"]})

if __name__ == '__main__':
    unittest.main()