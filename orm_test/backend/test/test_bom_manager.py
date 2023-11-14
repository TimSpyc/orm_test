

from backend.models.reference_models import User
from backend.src.manager.bill_of_material_manager import BillOfMaterial, BillOfMaterialGroup, BillOfMaterialManager
from backend.src.manager.derivative_constellium_manager import DerivativeConstelliumGroup
from backend.src.manager.project_manager import ProjectGroup
from django.test import TestCase
from datetime import datetime



class TestCheckIfIsInside(TestCase):
    def test_inside_case(self):
        result =  BillOfMaterialManager._BillOfMaterialManager__checkIfIsInside(1, 5, 2, 4) 
        self.assertTrue(result)

    def test_outside_case(self):
        result =  BillOfMaterialManager._BillOfMaterialManager__checkIfIsInside(1, 5, 0, 6) 
        self.assertFalse(result)

    def test_partial_inside_case(self):
        result =  BillOfMaterialManager._BillOfMaterialManager__checkIfIsInside(0, 7, 5, 10)
        self.assertFalse(result)


class TestCheckIfIsDirectChildNode(TestCase):
    def test_direct_child_case(self):
        node_list = [
            {'left': 2, 'right': 5},
            {'left': 6, 'right': 9},
            {'left': 3, 'right': 4}
        ]
        result = BillOfMaterialManager.\
        _BillOfMaterialManager__checkIfIsDirectChildNode(node_list, 1, 10, 2, 5) 
        self.assertTrue(result)

    def test_not_direct_child_case(self):
        node_list = [
            {'left': 2, 'right': 5},
            {'left': 6, 'right': 9},
        ]
        result = BillOfMaterialManager.\
            _BillOfMaterialManager__checkIfIsDirectChildNode(node_list, 1, 10, 7, 4) 
        self.assertFalse(result)
    
    def test_partly__is_direct_child_case(self):
        node_list = [
            {'left': 2, 'right': 5},
            {'left': 6, 'right': 9},
        ]
        result = BillOfMaterialManager.\
            _BillOfMaterialManager__checkIfIsDirectChildNode(node_list, 7, 10, 7, 4) 
        self.assertTrue(result)


class TestCheckIfIsLeafNode:
    def test_leaf_case(self):
        result = BillOfMaterialManager.\
            _BillOfMaterialManager___checkIfIsLeafNode(2, 3)
        self.assertTrue(result)

    def test_non_leaf_case(self):
        result = BillOfMaterialManager.\
            _BillOfMaterialManager___checkIfIsLeafNode(2, 4)
        self.assertFalse(result)


class TestAddHeadNodeToRelevantNodeList(TestCase):
    def setUp(self):
        self.project_group = ProjectGroup.objects.create()
        self.derivative_constellium_group = DerivativeConstelliumGroup.objects.create(
            project_group=self.project_group)
        self.bill_of_material_group = BillOfMaterialGroup.objects.create(
            derivative_constellium_group=self.derivative_constellium_group
        )
        self.manager = BillOfMaterialManager.__new__(BillOfMaterialManager)
        self.manager.group_id = self.bill_of_material_group.id

    def test_add_head_node(self):
        head_node = {'left_value': 2, 'right_value': 5}
        key_tuple = ('left_value', 'right_value')
        relevant_node_list = [
            {'left': 1, 'right': 3},
            {'left': 4, 'right': 7}
        ]
        result = self.manager._BillOfMaterialManager__addHeadNodeToRelevantNodeList(head_node, key_tuple, relevant_node_list)
        expected_result = [
            {'left': 1, 'right': 3},
            {'left': 4, 'right': 7},
            {'left_value': 2, 'right_value': 5, 'left': 2, 'right': 5, 'relative_quantity': 1}
        ]   
        self.assertEqual(result, expected_result)


    def test_add_head_node_empty_relevant_node_list(self):
        head_node = {'left_value': 2, 'right_value': 5}
        key_tuple = ('left_value', 'right_value')
        relevant_node_list = []
        result = self.manager._BillOfMaterialManager__addHeadNodeToRelevantNodeList(head_node, key_tuple, relevant_node_list)
        expected_result = [
            {'left_value': 2, 'right_value': 5, 'left': 2, 'right': 5, 'relative_quantity': 1}
        ]
        self.assertEqual(result, expected_result)
    

class TestSelectBomType(TestCase):
    def setUp(self):
        self.head_part_group_id = 1
        self.project_group = ProjectGroup.objects.create()
        self.derivative_constellium_group = DerivativeConstelliumGroup.objects.create(
            project_group=self.project_group)
        self.bill_of_material_group = BillOfMaterialGroup.objects.create(
            derivative_constellium_group=self.derivative_constellium_group
        )
        self.manager = BillOfMaterialManager.__new__(BillOfMaterialManager)
        self.manager.group_id = self.bill_of_material_group.id
        
    def test_select_bom_type_pd(self):

        left, right = self.manager._BillOfMaterialManager__selectBomType('pd')
        self.assertEqual(left, 'left_value_product_development')
        self.assertEqual(right, 'right_value_product_development')

    def test_select_bom_type_ai(self):
        left, right = self.manager._BillOfMaterialManager__selectBomType('ai')
        self.assertEqual(left, 'left_value_process_development')
        self.assertEqual(right, 'right_value_process_development')

    def test_select_bom_type_lg(self):
        left, right = self.manager._BillOfMaterialManager__selectBomType('lg')
        self.assertEqual(left, 'left_value_logistics')
        self.assertEqual(right, 'right_value_logistics')

    def test_select_bom_type_invalid(self):
        with self.assertRaises(ValueError):
            self.manager._BillOfMaterialManager__selectBomType('invalid_type')


class TestGetChildNodeList(TestCase):

    def setUp(self):
        self.project_group = ProjectGroup.objects.create()
        self.derivative_constellium_group = DerivativeConstelliumGroup.objects.create(
            project_group=self.project_group)
        self.bill_of_material_group = BillOfMaterialGroup.objects.create(
            derivative_constellium_group=self.derivative_constellium_group
        )
        self.manager = BillOfMaterialManager.__new__(BillOfMaterialManager)
        self.manager.group_id = self.bill_of_material_group.id
       
        self.bill_of_material_structure_dict_list = [
            {'left': 1, 'right': 6, 'cumulated_quantity': 100},
            {'left': 2, 'right': 3, 'cumulated_quantity': 20},
            {'left': 4, 'right': 5, 'cumulated_quantity': 30},
        ]
        self.manager.bill_of_material_structure_dict_list = self.bill_of_material_structure_dict_list

    def test_get_child_node_list_must_not_be_a_direct_child(self):

        parent_node = {'left': 1, 'right': 6, 'cumulated_quantity': 100}
        result = self.manager._BillOfMaterialManager__getChildNodeList(
            parent_node,
            ('left', 'right'),
            must_be_leaf=True,
            must_be_direct_child=False
        )
        expected_result = [{'left': 2, 'right': 3, 'cumulated_quantity': 20, 'relative_quantity': 0.2},
                           {'left': 4, 'right': 5, 'cumulated_quantity': 30, 'relative_quantity': 0.3}]
        self.assertEqual(result, expected_result)

    def test_get_child_node_list_must_be_a_direct_child(self):
        parent_node = {'left': 1, 'right': 6, 'cumulated_quantity': 100}
        result = self.manager._BillOfMaterialManager__getChildNodeList(
            parent_node,
            ('left', 'right'),
            must_be_leaf=True,
            must_be_direct_child=True
        )
        expected_result = [{'left': 2, 'right': 3, 'cumulated_quantity': 20, 'relative_quantity': 0.2}]
        self.assertEqual(result, expected_result)


class TestGetNodeHeadNodeList(TestCase): 
    def setUp(self):
        self.head_part_group_id = 1
        self.project_group = ProjectGroup.objects.create()
        self.derivative_constellium_group = DerivativeConstelliumGroup.objects.create(
            project_group=self.project_group)
        self.bill_of_material_group = BillOfMaterialGroup.objects.create(
            derivative_constellium_group=self.derivative_constellium_group
        )
        self.manager = BillOfMaterialManager.__new__(BillOfMaterialManager)
        self.manager.group_id = self.bill_of_material_group.id  
        self.manager.bill_of_material_structure_dict_list = [
        {'part_group': {'id': 1},'left_value_product_development': 1,'left': 1, 'right':4,},
        {'part_group': {'id': 2},'left_value_product_development': 1,'left': 2, 'right':3,},
        {'part_group': {'id': 3},'left_value_product_development': 1,'left': 5, 'right':10,},
        {'part_group': {'id': 4},'left_value_product_development': 1,'left': 6, 'right':9,},
        {'part_group': {'id': 5},'left_value_product_development': 1,'left': 7, 'right':8,},
        {'part_group': {'id': 6},'left_value_product_development': 1,'left': 11, 'right':18,},
        {'part_group': {'id': 7},'left_value_product_development': 1,'left': 12, 'right':17,},
        {'part_group': {'id': 8},'left_value_product_development': 1,'left': 13, 'right':16,},
        {'part_group': {'id': 9},'left_value_product_development': 1,'left': 14, 'right':15,},
    ]

    def test_get_node_head_node_list(self):      
        key_tuple = ('left', 'right')
        result = self.manager._BillOfMaterialManager__getNodeHeadNodeList(key_tuple)
        expected_result = [
            {'part_group': {'id': 1},'left_value_product_development': 1,'left': 1, 'right':4,},
            {'part_group': {'id': 3},'left_value_product_development': 1,'left': 5, 'right':10,},
            {'part_group': {'id': 6},'left_value_product_development': 1,'left': 11, 'right':18,},
            ]
        self.assertEqual(result, expected_result)


class TestGetHeadNodeList(TestCase):
    def setUp(self):
        self.head_part_group_id = 1
        self.project_group = ProjectGroup.objects.create()
        self.derivative_constellium_group = DerivativeConstelliumGroup.objects.create(
            project_group=self.project_group)
        self.bill_of_material_group = BillOfMaterialGroup.objects.create(
            derivative_constellium_group=self.derivative_constellium_group
        )
        self.manager = BillOfMaterialManager.__new__(BillOfMaterialManager)
        self.manager.group_id = self.bill_of_material_group.id
        self.manager.bill_of_material_structure_dict_list = [
        {'part_group': {'id': 1},'left_value_product_development': 1,'left': 1, 'right':4,},
        {'part_group': {'id': 2},'left_value_product_development': 2,'left': 2, 'right':3,},
        {'part_group': {'id': 3},'left_value_product_development': 3,'left': 5, 'right':10,},
        {'part_group': {'id': 4},'left_value_product_development': 4,'left': 6, 'right':9,},
        {'part_group': {'id': 5},'left_value_product_development': 5,'left': 7, 'right':8,},
        {'part_group': {'id': 6},'left_value_product_development': 6,'left': 11, 'right':18,},
        {'part_group': {'id': 7},'left_value_product_development': 7,'left': 12, 'right':17,},
        {'part_group': {'id': 8},'left_value_product_development': 8,'left': 13, 'right':16,},
        {'part_group': {'id': 9},'left_value_product_development': 9,'left': 14, 'right':15,},
    ]
        self.key_tuple = ('left', 'right')

    def test_get_head_node_with_id(self):
        result = self.manager._BillOfMaterialManager__getHeadNodeList(2, self.key_tuple)
        expected_result = [{'part_group': {'id': 2},'left_value_product_development': 2, 'left': 2, 'right': 3}]
        self.assertEqual(result, expected_result)

    def test_get_head_node_without_id(self):
        result = self.manager._BillOfMaterialManager__getHeadNodeList(None,self.key_tuple)
        expected_result = [
            {'part_group': {'id': 1},'left_value_product_development': 1, 'left': 1, 'right': 4},
            {'part_group': {'id': 3},'left_value_product_development': 3,'left': 5, 'right':10,},
            {'part_group': {'id': 6},'left_value_product_development': 6, 'left': 11, 'right': 18},
        ]
        self.assertEqual(result, expected_result)
        
    def test_get_head_node_not_existing_id(self):
        with self.assertRaises(ValueError):
            result = self.manager._BillOfMaterialManager__getHeadNodeList(10,self.key_tuple)


class TestCheckBillOfMaterialPositionStructure(TestCase):
    def check_bill_of_material_position_structure_invalid_format(self):
        input_data = 'invalid format'
            
        with self.assertRaises(ValueError):
            sorted_and_formatted = BillOfMaterialManager._checkBillOfMaterialPositionStructure(input_data)

    def check_bill_of_material_position_structure_missing_key_group_in_dict(self):
        input_data = input_data = [
            {'pos': '2.1.1'},
        ]
        with self.assertRaises(ValueError):
            sorted_and_formatted = BillOfMaterialManager._checkBillOfMaterialPositionStructure(input_data)

    def check_bill_of_material_position_structure_missing_key_pos_in_dict(self):
        input_data = input_data = [
            {'group_id': 21},
        ]
        with self.assertRaises(ValueError):
            sorted_and_formatted = BillOfMaterialManager._checkBillOfMaterialPositionStructure(input_data)

    def check_bill_of_material_position_structure_no_dict_in_list(self):
        input_data = input_data = [[]]
        with self.assertRaises(ValueError):
            sorted_and_formatted = BillOfMaterialManager._checkBillOfMaterialPositionStructure(input_data)

    def check_bill_of_material_position_structure_empty_list(self):
        input_data = input_data = []
        with self.assertRaises(ValueError):
            sorted_and_formatted = BillOfMaterialManager._checkBillOfMaterialPositionStructure(input_data)


class TestSortPositionStructure(TestCase):
    def test_sort_position_structure(self):
        input_data = [
            {'pos': '2.1.1', 'group_id': 1},
            {'pos': '2.1', 'group_id': 2},
            {'pos': '2', 'group_id': 20},
            {'pos': '1', 'group_id': 21},
            {'pos': '1.1', 'group_id': 21},
        ]
        sorted_and_formatted = BillOfMaterialManager._sortPositionStructure(input_data)
        expected_output = [
            {'pos': '1', 'group_id': 21},
            {'pos': '1.1', 'group_id': 21}, 
            {'pos': '2', 'group_id': 20}, 
            {'pos': '2.1', 'group_id': 2}, 
            {'pos': '2.1.1', 'group_id': 1}
            ]
        self.assertEqual(sorted_and_formatted, expected_output)

    def test_sort_position_structure_one_head(self):
        input_data = [
            {'pos': '1.2', 'group_id': 1},
            {'pos': '1.3', 'group_id': 2},
            {'pos': '1.3.1', 'group_id': 20},
            {'pos': '1', 'group_id': 12},
            {'pos': '1.1', 'group_id': 21},
        ]
        sorted_and_formatted = BillOfMaterialManager._sortPositionStructure(input_data)
        expected_output = [
            {'pos': '1', 'group_id': 12},
            {'pos': '1.1', 'group_id': 21}, 
            {'pos': '1.2', 'group_id': 1}, 
            {'pos': '1.3', 'group_id': 2}, 
            {'pos': '1.3.1', 'group_id': 20}
            ]
        self.assertEqual(sorted_and_formatted, expected_output)


class TestHeadCheckOfBillOfMaterialPositionStructure(TestCase):

    def test_head_check_of_bill_of_material_position_structure_no_missing_head(self):
        input_data = [
            {'pos': '2.1', 'group_id': 2},
            {'pos': '2.1.1', 'group_id': 1},
            {'pos': '2', 'group_id': 20},
            {'pos': '1', 'group_id': 21},
        ]
        sorted_and_formatted = BillOfMaterialManager._headCheckOfBillOfMaterialPositionStructure(input_data)
        expected_output = [
            {'pos': '1', 'group_id': 21},
            {'pos': '2', 'group_id': 20}, 
            {'pos': '2.1', 'group_id': 2}, 
            {'pos': '2.1.1', 'group_id': 1},
            ]
        self.assertEqual(sorted_and_formatted, expected_output)


    def test_head_check_of_bill_of_material_position_structure_missing_head(self):
        input_data = [
            {'pos': '2.1.1', 'group_id': 1},
            {'pos': '2.1', 'group_id': 2},
            #{'pos': '2', 'group_id': 20},
            {'pos': '1', 'group_id': 21},
        ]
        with self.assertRaises(ValueError):
            sorted_and_formatted = BillOfMaterialManager._headCheckOfBillOfMaterialPositionStructure(input_data)


class TestCreateNestedSet(TestCase):
    def test_created_nested_set(self):
        sorted_input_data = [
            {'pos': '1', 'group_id': 21},
            {'pos': '2', 'group_id': 20},
            {'pos': '2.1', 'group_id': 2},
            {'pos': '2.1.1', 'group_id': 1},
        ]
        expected_output = [
            {'group_id': 21, 'left': 1, 'right': 2},
            {'group_id': 20, 'left': 3, 'right': 8},
            {'group_id': 2, 'left': 4, 'right': 7},
            {'group_id': 1, 'left': 5, 'right': 6},
        ]
        result = BillOfMaterialManager._createNestedSet(sorted_input_data)
        self.assertEqual(result, expected_output)

    def test_created_nested_set_one_head(self):
        sorted_input_data = [
            {'pos': '2', 'group_id': 20},
            {'pos': '2.1', 'group_id': 2},
            {'pos': '2.1.1', 'group_id': 1},
        ]
        expected_output = [
            {'group_id': 20, 'left': 1, 'right': 6},
            {'group_id': 2, 'left': 2, 'right': 5},
            {'group_id': 1, 'left': 3, 'right': 4},
        ]
        result = BillOfMaterialManager._createNestedSet(sorted_input_data)
        self.assertEqual(result, expected_output)


class TestFormatBillOfMaterialPositionStructureToNestedSet(TestCase):
     
     def test_format_bill_of_material_position_structure_to_nested_set(self):
        input_data = [
            {'pos': '2.1.1', 'group_id': 1},
            {'pos': '2.1', 'group_id': 2},
            {'pos': '2', 'group_id': 20},
            {'pos': '1', 'group_id': 21},
        ]
        expected_output = [
            {'group_id': 21, 'left': 1, 'right': 2},
            {'group_id': 20, 'left': 3, 'right': 8},
            {'group_id': 2, 'left': 4, 'right': 7},
            {'group_id': 1, 'left': 5, 'right': 6},
        ]
        result = BillOfMaterialManager.formatBillOfMaterialPositionStructureToNestedSet(input_data)
        self.assertEqual(result, expected_output)

     def test_format_bill_of_material_position_structure_to_nested_set_same_head(self):
        input_data = [
        {'pos': '1', 'group_id': 1},
        {'pos': '1.1', 'group_id': 2},
        {'pos': '1.2', 'group_id': 20},
        {'pos': '1.3', 'group_id': 21},
        {'pos': '1.3.1', 'group_id': 22},
        ] 
        expected_output = [
            {'group_id': 1, 'left': 1, 'right': 10}, 
            {'group_id': 2, 'left': 2, 'right': 3}, 
            {'group_id': 20, 'left': 4, 'right': 5}, 
            {'group_id': 21, 'left': 6, 'right': 9}, 
            {'group_id': 22, 'left': 7, 'right': 8}
        ]
        result = BillOfMaterialManager.formatBillOfMaterialPositionStructureToNestedSet(input_data)
        self.assertEqual(result, expected_output) 

     def test_format_bill_of_material_position_structure_to_nested_set_invalid_input(self):
        input_data = 'invald input'
        with self.assertRaises(ValueError):
            result = BillOfMaterialManager.formatBillOfMaterialPositionStructureToNestedSet(input_data)

     def test_format_bill_of_material_position_structure_to_nested_set_missing_head(self):
        input_data = [
        {'pos': '1.1', 'group_id': 2},
        {'pos': '1.2', 'group_id': 20},
        ] 
        with self.assertRaises(ValueError):
            result = BillOfMaterialManager.formatBillOfMaterialPositionStructureToNestedSet(input_data)



class TestCheckBillOfMaterialNestedSet(TestCase):

    def test_check_bill_of_material_nested_set_invalid_format(self):
        input_data = 'invalid format'
        with self.assertRaises(ValueError):
            result = BillOfMaterialManager._checkBillOfMaterialNestedSet(input_data)

    def test_check_bill_of_material_nested_set_missing_key_group_id_in_dict(self):
        input_data = input_data = [
            {'left': 1, 'right': 2},
        ]
        with self.assertRaises(ValueError):
            result = BillOfMaterialManager._checkBillOfMaterialNestedSet(input_data)

    def test_check_bill_of_material_position_structure_missing_key_left_in_dict(self):
        input_data = input_data = [
            {'group_id': 21, 'right': 2},
            ]
        with self.assertRaises(ValueError):
            result = BillOfMaterialManager._checkBillOfMaterialNestedSet(input_data)

    def test_check_bill_of_material_position_structure_missing_key_right_in_dict(self):
        input_data = input_data = [
            {'group_id': 21, 'left': 2},
            ]
        with self.assertRaises(ValueError):
            result = BillOfMaterialManager._checkBillOfMaterialNestedSet(input_data)

    def test_check_bill_of_material_position_structure_no_dict_in_list(self):
        input_data = input_data = [[]]
        with self.assertRaises(ValueError):
            result = BillOfMaterialManager._checkBillOfMaterialNestedSet(input_data)

    def test_check_bill_of_material_position_structure_empty_list(self):
        input_data = input_data = []
        with self.assertRaises(ValueError):
            result = BillOfMaterialManager._checkBillOfMaterialNestedSet(input_data)


class TestCheckValuesBillOfMaterialNestedSet(TestCase):

    def test_valid_nested_set(self):
        valid_nested_set_data = [
            {'group_id': 21, 'left': 1, 'right': 2},
            {'group_id': 20, 'left': 3, 'right': 8},
            {'group_id': 2, 'left': 4, 'right': 7},
            {'group_id': 1, 'left': 5, 'right': 6},
        ]
        result = BillOfMaterialManager._checkValuesBillOfMaterialNestedSet(valid_nested_set_data)
        self.assertTrue(result)

    def test_invalid_left_greater_than_right(self):
        invalid_nested_set_data = [
            {'group_id': 1, 'left': 3, 'right': 2},
            {'group_id': 2, 'left': 3, 'right': 3},
        ]
        with self.assertRaises(ValueError):
            result = BillOfMaterialManager._checkValuesBillOfMaterialNestedSet(invalid_nested_set_data)


    def test_invalid_left_equal_to_right(self):
        invalid_nested_set_data = [
            {'group_id': 1, 'left': 1, 'right': 1},
            {'group_id': 2, 'left': 2, 'right': 2},
        ]
        with self.assertRaises(ValueError):
            result = BillOfMaterialManager._checkValuesBillOfMaterialNestedSet(invalid_nested_set_data)

    def test_invalid_left_overlapping(self):
        invalid_nested_set_data = [
            {'group_id': 1, 'left': 1, 'right': 2},
            {'group_id': 2, 'left': 2, 'right': 3},
        ]
        with self.assertRaises(ValueError):
            result = BillOfMaterialManager._checkValuesBillOfMaterialNestedSet(invalid_nested_set_data)

    def test_invalid_nested_set_structure(self):
        invalid_nested_set_data = [
            {'group_id': 1, 'left': 1, 'right': 6},
            {'group_id': 2, 'left': 2, 'right': 5},
        ]
        with self.assertRaises(ValueError):
            result = BillOfMaterialManager._checkValuesBillOfMaterialNestedSet(invalid_nested_set_data)

    def test_invalid_nested_set_structure_diff_more_than_one(self):
        invalid_nested_set_data = [
            {'group_id': 1, 'left': 1, 'right': 2},
            {'group_id': 2, 'left': 3, 'right': 5},
        ]
        with self.assertRaises(ValueError):
            result = BillOfMaterialManager._checkValuesBillOfMaterialNestedSet(invalid_nested_set_data)


class TestSortNestedSet(TestCase):
    def test_sorted_nested_set(self):
            nested_set_data = [
                {'group_id': 4, 'left': 7, 'right': 8},
                {'group_id': 2, 'left': 2, 'right': 3},
                {'group_id': 1, 'left': 1, 'right': 6},
                {'group_id': 3, 'left': 4, 'right': 5},
            ]
            expected_output = [
                {'pos': '1', 'group_id': 1},
                {'pos': '1.1', 'group_id': 2},
                {'pos': '1.2', 'group_id': 3},
                {'pos': '2', 'group_id': 4},

            ]
            result = BillOfMaterialManager._createPositionStructure(nested_set_data)
            self.assertEqual(result, expected_output)


class TestFormatBillOfMaterialNestedSetToPositionStructure(TestCase):

    def test_format_nested_set_to_bom_structure(self):
        nested_set_data = [
            {'group_id': 21, 'left': 1, 'right': 2},
            {'group_id': 20, 'left': 3, 'right': 8},
            {'group_id': 2, 'left': 4, 'right': 7},
            {'group_id': 1, 'left': 5, 'right': 6},
        ]
        expected_output = [
            {'pos': '1', 'group_id': 21},
            {'pos': '2', 'group_id': 20},
            {'pos': '2.1', 'group_id': 2},
            {'pos': '2.1.1', 'group_id': 1},
        ]
        result = BillOfMaterialManager.formatBillOfMaterialNestedSetToPositionStructure(nested_set_data)
        self.assertEqual(result, expected_output)

    def test_format_nested_set_to_bom_structure_one_head_node(self):
        nested_set_data = [
            {'group_id': 1, 'left': 1, 'right': 10}, 
            {'group_id': 2, 'left': 2, 'right': 3}, 
            {'group_id': 20, 'left': 4, 'right': 5}, 
            {'group_id': 21, 'left': 6, 'right': 9}, 
            {'group_id': 22, 'left': 7, 'right': 8}
        ]
        expected_output = [
        {'pos': '1', 'group_id': 1},
        {'pos': '1.1', 'group_id': 2},
        {'pos': '1.2', 'group_id': 20},
        {'pos': '1.3', 'group_id': 21},
        {'pos': '1.3.1', 'group_id': 22},
        ] 
        result = BillOfMaterialManager.formatBillOfMaterialNestedSetToPositionStructure(nested_set_data)
        self.assertEqual(result, expected_output)

    def test_format_nested_set_to_bom_structure_mixed_input(self):
        nested_set_data = [
            {'group_id': 1, 'left': 1, 'right': 6}, 
            {'group_id': 2, 'left': 2, 'right': 3}, 
            {'group_id': 20, 'left': 4, 'right': 5}, 
        ]
        expected_output = [
        {'pos': '1', 'group_id': 1},
        {'pos': '1.1', 'group_id': 2},
        {'pos': '1.2', 'group_id': 20}
        ]
        result = BillOfMaterialManager.formatBillOfMaterialNestedSetToPositionStructure(nested_set_data)
        self.assertEqual(result, expected_output)

    def test_format_nested_set_to_bom_structure_duplicate_values(self):
            nested_set_data = [
                {'group_id': 1, 'left': 1, 'right': 6}, 
                {'group_id': 2, 'left': 2, 'right': 3}, 
                {'group_id': 21, 'left': 5, 'right': 6}, 
            ]
            expected_output = [
            {'pos': '1', 'group_id': 1},
            {'pos': '1.1', 'group_id': 2},
            {'pos': '1.3', 'group_id': 21},
            ] 
            with self.assertRaises(ValueError):
                result = BillOfMaterialManager.formatBillOfMaterialNestedSetToPositionStructure(nested_set_data)

    def test_format_nested_set_to_bom_structure_long(self):
        nested_set_data = [
            {'group_id': 21, 'left': 1, 'right': 2},
            {'group_id': 20, 'left': 3, 'right': 8},
            {'group_id': 2, 'left': 4, 'right': 7},
            {'group_id': 1, 'left': 5, 'right': 6},

            {'group_id': 3, 'left': 9, 'right': 18 },
            {'group_id': 4, 'left': 10, 'right': 17},
            {'group_id': 5, 'left': 11, 'right': 12},
            {'group_id': 6, 'left': 13, 'right': 14},
            {'group_id': 7, 'left': 15, 'right': 16},

            {'group_id': 8, 'left': 19, 'right': 22},
            {'group_id': 9, 'left': 20, 'right': 21},
        ]
        expected_output = [
            {'pos': '1', 'group_id': 21},
            {'pos': '2', 'group_id': 20},
            {'pos': '2.1', 'group_id': 2},
            {'pos': '2.1.1', 'group_id': 1},
            {'pos': '3', 'group_id': 3},
            {'pos': '3.1', 'group_id': 4},
            {'pos': '3.1.1', 'group_id': 5},
            {'pos': '3.1.2', 'group_id': 6},
            {'pos': '3.1.3', 'group_id': 7},
            {'pos': '4', 'group_id': 8},
            {'pos': '4.1', 'group_id': 9},
        ]
        result = BillOfMaterialManager.formatBillOfMaterialNestedSetToPositionStructure(nested_set_data)
        self.assertEqual(result, expected_output)



class TestCreatePositionStructure(TestCase):
            
    def test_create_position_structure(self):
            nested_set_data = [
                {'group_id': 1, 'left': 1, 'right': 6},
                {'group_id': 2, 'left': 2, 'right': 3},
                {'group_id': 3, 'left': 4, 'right': 5},
                {'group_id': 4, 'left': 7, 'right': 8},

            ]
            expected_output = [
                {'pos': '1', 'group_id': 1},
                {'pos': '1.1', 'group_id': 2},
                {'pos': '1.2', 'group_id': 3},
                {'pos': '2', 'group_id': 4},

            ]
            result = BillOfMaterialManager._createPositionStructure(nested_set_data)
            self.assertEqual(result, expected_output)

    def test_create_position_structure_one_head(self):
            nested_set_data = [
                {'group_id': 1, 'left': 1, 'right': 6},
                {'group_id': 2, 'left': 2, 'right': 3},
                {'group_id': 3, 'left': 4, 'right': 5},
            ]
            expected_output = [
                {'pos': '1', 'group_id': 1},
                {'pos': '1.1', 'group_id': 2},
                {'pos': '1.2', 'group_id': 3},
            ]
            result = BillOfMaterialManager._createPositionStructure(nested_set_data)
            self.assertEqual(result, expected_output)

    def test_create_position_structure_not_right_order(self):
            nested_set_data = [
                {'group_id': 1, 'left': 1, 'right': 6},
                {'group_id': 3, 'left': 4, 'right': 5},
                {'group_id': 2, 'left': 2, 'right': 3},
            ]
            expected_output = [
                {'pos': '1', 'group_id': 1},
                {'pos': '1.1', 'group_id': 2},
                {'pos': '1.2', 'group_id': 3},
            ]
            result = BillOfMaterialManager._createPositionStructure(nested_set_data)
            self.assertEqual(result, expected_output)

    def test_create_position_structure_long(self):
        nested_set_data = [
            {'group_id': 21, 'left': 1, 'right': 2},
            {'group_id': 20, 'left': 3, 'right': 8},
            {'group_id': 2, 'left': 4, 'right': 7},
            {'group_id': 1, 'left': 5, 'right': 6},

            {'group_id': 3, 'left': 9, 'right': 18 },
            {'group_id': 4, 'left': 10, 'right': 17},
            {'group_id': 5, 'left': 11, 'right': 12},
            {'group_id': 6, 'left': 13, 'right': 14},
            {'group_id': 7, 'left': 15, 'right': 16},

            {'group_id': 8, 'left': 19, 'right': 22},
            {'group_id': 9, 'left': 20, 'right': 21},
        ]
        expected_output = [
            {'pos': '1', 'group_id': 21},
            {'pos': '2', 'group_id': 20},
            {'pos': '2.1', 'group_id': 2},
            {'pos': '2.1.1', 'group_id': 1},
            {'pos': '3', 'group_id': 3},
            {'pos': '3.1', 'group_id': 4},
            {'pos': '3.1.1', 'group_id': 5},
            {'pos': '3.1.2', 'group_id': 6},
            {'pos': '3.1.3', 'group_id': 7},
            {'pos': '4', 'group_id': 8},
            {'pos': '4.1', 'group_id': 9},
        ]
        result = BillOfMaterialManager._createPositionStructure(nested_set_data)
        self.assertEqual(result, expected_output)

        
class Test__GetBillOfMaterialStructure(TestCase):  
    def setUp(self):
        self.head_part_group_id = 1
        self.project_group = ProjectGroup.objects.create()
        self.derivative_constellium_group = DerivativeConstelliumGroup.objects.create(
            project_group=self.project_group)
        self.bill_of_material_group = BillOfMaterialGroup.objects.create(
            derivative_constellium_group=self.derivative_constellium_group
        )
        self.manager = BillOfMaterialManager.__new__(BillOfMaterialManager)
        self.manager.group_id = self.bill_of_material_group.id
        self.manager.bill_of_material_structure_dict_list = [
            {'group_id': 1, 'left': 1, 'right': 6, 'cumulated_quantity': 100},
            {'group_id': 2, 'left': 2, 'right': 3, 'cumulated_quantity': 20},
            {'group_id': 3,'left': 4, 'right': 5, 'cumulated_quantity': 30},
            {'group_id': 4,'left': 7, 'right': 8, 'cumulated_quantity': 40},
        ]

    def test_get_bill_of_material_structure_first_head(self):
        head_node = {
            'group_id': 1,
            'left': 1, 
            'right': 6, 
            'cumulated_quantity': 100
            }
        result= self.manager._BillOfMaterialManager__getBillOfMaterialStructure(head_node, ('left', 'right',))
        expected_result = [{'pos': '1', 'group_id': 1}, {'pos': '1.1', 'group_id': 2}, {'pos': '1.2', 'group_id': 3}]
        self.assertEqual(expected_result, result)

        
    def test_get_bill_of_material_structure_missing_key_group(self):
        head_node = {
            #'group_id': 1, 
            'left': 1, 
            'right': 6, 
            'cumulated_quantity': 100
            }
        with self.assertRaises(ValueError):
            result = self.manager._BillOfMaterialManager__getBillOfMaterialStructure(head_node, ('left', 'right'))

    def test_get_bill_of_material_structure_invalid_structure(self):
        self.manager.bill_of_material_structure_dict_list = [
            {'group_id': 1, 'left': 1, 'right': 6, 'cumulated_quantity': 100},
            {'group_id': 2, 'left': 2, 'right': 4, 'cumulated_quantity': 20},
            {'group_id': 3, 'left': 5, 'right': 7, 'cumulated_quantity': 30},
            {'group_id': 4, 'left': 8, 'right': 10, 'cumulated_quantity': 40},
        ]
        head_node = {
            'group_id': 1,
            'left': 1,
            'right': 6,
            'cumulated_quantity': 100
        }
        with self.assertRaises(ValueError):
            result = self.manager._BillOfMaterialManager__getBillOfMaterialStructure(head_node, ('left', 'right'))

   

class TestGetBillOfMaterialDetails(TestCase):
    def setUp(self):
        self.project_group = ProjectGroup.objects.create()
        self.derivative_constellium_group = DerivativeConstelliumGroup.objects.create(
            project_group=self.project_group)
        self.bill_of_material_group = BillOfMaterialGroup.objects.create(
            derivative_constellium_group=self.derivative_constellium_group
        )
        self.manager = BillOfMaterialManager.__new__(BillOfMaterialManager)
        self.manager.group_id = self.bill_of_material_group.id

    def test_get_bill_of_material_details_for_bom_type_pd(self):
        self.manager.bill_of_material_structure_dict_list = [
        {'part_group': {'id': 1},'left_value_product_development': 1,"right_value_product_development" : 4,'cumulated_quantity': 100, 'left': 1, 'right':4,'group_id': 4},
        {'part_group': {'id': 2},'left_value_product_development': 2,"right_value_product_development" : 3,'cumulated_quantity': 20, 'left': 2, 'right':3,'group_id': 3},
        {'part_group': {'id': 3},'left_value_product_development': 3,"right_value_product_development" : 10,'cumulated_quantity': 30, 'left': 5, 'right':10,'group_id': 2},
        {'part_group': {'id': 4},'left_value_product_development': 4,"right_value_product_development" : 9,'cumulated_quantity': 40, 'left': 6, 'right':9,'group_id': 1},
     ]
        bom_type = "pd"
        head_part_group_id = 1  
        result = self.manager.getBillOfMaterialDetails(bom_type, head_part_group_id)
        expected_result = [
            {'head_node': 
             {'part_group': {'id': 1}, 'left_value_product_development': 1, 'right_value_product_development': 4, 'cumulated_quantity': 100, 'left': 1, 'right': 4, 'group_id': 4},
              'direct_child_node_list': 
              [{'part_group': {'id': 2}, 'left_value_product_development': 2, 'right_value_product_development': 3, 'cumulated_quantity': 20, 'left': 2, 'right': 3, 'group_id': 3, 'relative_quantity': 0.2}],
                'leaf_node_list': [{'part_group': {'id': 2}, 'left_value_product_development': 2, 'right_value_product_development': 3, 'cumulated_quantity': 20, 'left': 2, 'right': 3, 'group_id': 3, 'relative_quantity': 0.2}],
                  'structure': [{'pos': '1', 'group_id': 4}, {'pos': '1.1', 'group_id': 3}]}
                  ]
        self.assertEqual(result, expected_result)

    def test_get_bill_of_material_details_for_bom_type_ai(self):
        self.manager.bill_of_material_structure_dict_list = [
        {'part_group': {'id': 1},'left_value_process_development': 1,"right_value_process_development" : 4,'cumulated_quantity': 100, 'left': 1, 'right':4,'group_id': 4},
        {'part_group': {'id': 2},'left_value_process_development': 2,"right_value_process_development" : 3,'cumulated_quantity': 20, 'left': 2, 'right':3,'group_id': 3},
        {'part_group': {'id': 3},'left_value_process_development': 3,"right_value_process_development" : 10,'cumulated_quantity': 30, 'left': 5, 'right':10,'group_id': 2},
        {'part_group': {'id': 4},'left_value_process_development': 4,"right_value_process_development" : 9,'cumulated_quantity': 40, 'left': 6, 'right':9,'group_id': 1},
     ]
        bom_type = "ai"
        head_part_group_id = 1  
        result = self.manager.getBillOfMaterialDetails(bom_type, head_part_group_id)
        expected_result = [
            {'head_node': {'part_group': {'id': 1}, 'left_value_process_development': 1, 'right_value_process_development': 4, 'cumulated_quantity': 100, 'left': 1, 'right': 4, 'group_id': 4},
              'direct_child_node_list': [{'part_group': {'id': 2}, 'left_value_process_development': 2, 'right_value_process_development': 3, 'cumulated_quantity': 20, 'left': 2, 'right': 3, 'group_id': 3, 'relative_quantity': 0.2}],
                'leaf_node_list': [{'part_group': {'id': 2}, 'left_value_process_development': 2, 'right_value_process_development': 3, 'cumulated_quantity': 20, 'left': 2, 'right': 3, 'group_id': 3, 'relative_quantity': 0.2}], 
                'structure': [{'pos': '1', 'group_id': 4}, {'pos': '1.1', 'group_id': 3}]}
                ]
        self.assertEqual(result, expected_result)

    def test_get_bill_of_material_details_for_bom_type_lg(self):
        self.manager.bill_of_material_structure_dict_list = [
        {'part_group': {'id': 1},'left_value_logistics': 1,"right_value_logistics" : 4,'cumulated_quantity': 100, 'left': 1, 'right':4,'group_id': 4},
        {'part_group': {'id': 2},'left_value_logistics': 2,"right_value_logistics" : 3,'cumulated_quantity': 20, 'left': 2, 'right':3,'group_id': 3},
        {'part_group': {'id': 3},'left_value_logistics': 3,"right_value_logistics" : 10,'cumulated_quantity': 30, 'left': 5, 'right':10,'group_id': 2},
        {'part_group': {'id': 4},'left_value_logistics': 4,"right_value_logistics" : 9,'cumulated_quantity': 40, 'left': 6, 'right':9,'group_id': 1},
     ]
        bom_type = "lg"
        head_part_group_id = 1  
        result = self.manager.getBillOfMaterialDetails(bom_type, head_part_group_id)
        expected_result = [
            {'head_node': {'part_group': {'id': 1}, 'left_value_logistics': 1, 'right_value_logistics': 4, 'cumulated_quantity': 100, 'left': 1, 'right': 4, 'group_id': 4},
              'direct_child_node_list': [{'part_group': {'id': 2}, 'left_value_logistics': 2, 'right_value_logistics': 3, 'cumulated_quantity': 20, 'left': 2, 'right': 3, 'group_id': 3, 'relative_quantity': 0.2}],
                'leaf_node_list': [{'part_group': {'id': 2}, 'left_value_logistics': 2, 'right_value_logistics': 3, 'cumulated_quantity': 20, 'left': 2, 'right': 3, 'group_id': 3, 'relative_quantity': 0.2}], 
                'structure': [{'pos': '1', 'group_id': 4}, {'pos': '1.1', 'group_id': 3}]}
                ]
        self.assertEqual(result, expected_result)

    def test_get_bill_of_material_details_no_head_part_group_id(self):
        self.manager.bill_of_material_structure_dict_list = [
        {'part_group': {'id': 1},'left_value_logistics': 1,"right_value_logistics" : 4,'cumulated_quantity': 100, 'left': 1, 'right':4,'group_id': 4},
        {'part_group': {'id': 2},'left_value_logistics': 2,"right_value_logistics" : 3,'cumulated_quantity': 20, 'left': 2, 'right':3,'group_id': 3},
        {'part_group': {'id': 3},'left_value_logistics': 5,"right_value_logistics" : 10,'cumulated_quantity': 30, 'left': 5, 'right':10,'group_id': 2},
        {'part_group': {'id': 4},'left_value_logistics': 6,"right_value_logistics" : 9,'cumulated_quantity': 40, 'left': 6, 'right':9,'group_id': 1},
        {'part_group': {'id': 4},'left_value_logistics': 7,"right_value_logistics" : 8,'cumulated_quantity': 40, 'left': 7, 'right':8,'group_id': 10},
     ]
        result = self.manager.getBillOfMaterialDetails(bom_type = "lg",head_part_group_id=None)
        expected_result = [
            {'head_node': {'part_group': {'id': 1}, 'left_value_logistics': 1, 'right_value_logistics': 4, 'cumulated_quantity': 100, 'left': 1, 'right': 4, 'group_id': 4}, 
             'direct_child_node_list': [{'part_group': {'id': 2}, 'left_value_logistics': 2, 'right_value_logistics': 3, 'cumulated_quantity': 20, 'left': 2, 'right': 3, 'group_id': 3, 'relative_quantity': 0.2}],
              'leaf_node_list': [{'part_group': {'id': 2}, 'left_value_logistics': 2, 'right_value_logistics': 3, 'cumulated_quantity': 20, 'left': 2, 'right': 3, 'group_id': 3, 'relative_quantity': 0.2}], 'structure': [{'pos': '1', 'group_id': 4}, {'pos': '1.1', 'group_id': 3}]},
                {'head_node': {'part_group': {'id': 3}, 'left_value_logistics': 5, 'right_value_logistics': 10, 'cumulated_quantity': 30, 'left': 5, 'right': 10, 'group_id': 2}, 'direct_child_node_list': [{'part_group': {'id': 4}, 'left_value_logistics': 6, 'right_value_logistics': 9, 'cumulated_quantity': 40, 'left': 6, 'right': 9, 'group_id': 1, 'relative_quantity': 1.3333333333333333}],
                  'leaf_node_list': [{'part_group': {'id': 4}, 'left_value_logistics': 7, 'right_value_logistics': 8, 'cumulated_quantity': 40, 'left': 7, 'right': 8, 'group_id': 10, 'relative_quantity': 1.3333333333333333}], 
                   'structure': [{'pos': '1', 'group_id': 2}, {'pos': '1.1', 'group_id': 1}, {'pos': '1.1.1', 'group_id': 10}]}
                   ]
        self.assertEqual(result, expected_result)

 