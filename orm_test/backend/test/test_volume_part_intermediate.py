import unittest
from unittest.mock import Mock, patch
from backend.src.intermediate import VolumePartIntermediate

class TestGetVolume(unittest.TestCase):
    @patch('volume_part_intermediate.VolumePartIntermediate.__updateTotalVolume', return_value=[])
    def test_simpleBomStructure(self, mock_update_total_volume):
        # Mocking the dependencies
        bom_manager = Mock()
        bom_manager.bill_of_material_structure_list_of_dict = [{'part_group_id': 1, 'cumulated_quantity': 10}]
        bom_manager.derivative_constellium_group_id = 1

        part_manager = Mock()
        part_manager.group_id = 1

        volume_derivative_intermediate_class = Mock()
        volume_derivative_intermediate_class.volume = 100

        # Creating an instance of the class and setting the dependencies
        instance = VolumePartIntermediate()
        instance.bom_manager_list = [bom_manager]
        instance.part_manager = part_manager
        instance.VolumeDerivativeIntermediateClass = Mock(return_value=volume_derivative_intermediate_class)
        instance.search_date = '2022-01-01'

        # Calling the function and checking the result
        result = instance.getVolume()
        expected_result = ([], [{'derivative_constellium_group_id': 1, 'volume_derivative': 100, 'cumulated_quantity': 10}])
        self.assertEqual(result, expected_result)

    @patch('volume_part_intermediate.VolumePartIntermediate.__updateTotalVolume', return_value=[])
    def test_complexBomStructure(self):
        # Mocking the dependencies
        bom_manager = Mock()
        bom_manager.bill_of_material_structure_list_of_dict = [
            {'part_group_id': 1, 'cumulated_quantity': 10},
            {'part_group_id': 2, 'cumulated_quantity': 10},
            {'part_group_id': 3, 'cumulated_quantity': 10},
            {'part_group_id': 4, 'cumulated_quantity': 10},
            {'part_group_id': 1, 'cumulated_quantity': 5}
        ]
        bom_manager.derivative_constellium_group_id = 1

        part_manager = Mock()
        part_manager.group_id = 1

        volume_derivative_intermediate_class = Mock()
        volume_derivative_intermediate_class.volume = 100

        # Creating an instance of the class and setting the dependencies
        instance = VolumePartIntermediate()
        instance.bom_manager_list = [bom_manager]
        instance.part_manager = part_manager
        instance.VolumeDerivativeIntermediateClass = Mock(return_value=volume_derivative_intermediate_class)
        instance.search_date = '2022-01-01'

        # Calling the function and checking the result
        result = instance.getVolume()
        expected_result = ([], [{'derivative_constellium_group_id': 1, 'volume_derivative': 100, 'cumulated_quantity': 15}])
        self.assertEqual(result, expected_result)


class TestUpdateTotalVolume(unittest.TestCase):
    def test_emptyList(self):
        # Mocking the GeneralIntermediate object and its volume attribute
        inter_obj = Mock()
        inter_obj.volume = [{'date': '2022-01-01', 'volume': 100}, {'date': '2022-01-02', 'volume': 200}]

        # Creating an instance of the class
        instance = VolumePartIntermediate()  # replace with your actual class name

        # Calling the function and checking the result
        total_volume = []
        cumulated_quantity = 2
        result = instance._VolumePartIntermediate__updateTotalVolume(total_volume, cumulated_quantity, inter_obj)
        expected_result = [{'date': '2022-01-01', 'volume': 200}, {'date': '2022-01-02', 'volume': 400}]
        self.assertEqual(result, expected_result)

    def test_prefilledList(self):
        # Mocking the GeneralIntermediate object and its volume attribute
        inter_obj = Mock()
        inter_obj.volume = [{'date': '2022-01-01', 'volume': 100}, {'date': '2022-01-02', 'volume': 200}]

        # Creating an instance of the class
        instance = VolumePartIntermediate()  # replace with your actual class name

        # Calling the function and checking the result
        total_volume = [{'date': '2022-01-01', 'volume': 200}, {'date': '2022-01-02', 'volume': 400}]
        cumulated_quantity = 2
        result = instance._VolumePartIntermediate__updateTotalVolume(total_volume, cumulated_quantity, inter_obj)
        expected_result = [{'date': '2022-01-01', 'volume': 400}, {'date': '2022-01-02', 'volume': 800}]
        self.assertEqual(result, expected_result)

    def test_negativVolume(self):
        # Mocking the GeneralIntermediate object and its volume attribute
        inter_obj = Mock()
        inter_obj.volume = [{'date': '2022-01-01', 'volume': -100}, {'date': '2022-01-02', 'volume': 200}]

        # Creating an instance of the class
        instance = VolumePartIntermediate()  # replace with your actual class name

        # Calling the function and checking the result
        total_volume = []
        cumulated_quantity = 2
        result = instance._VolumePartIntermediate__updateTotalVolume(total_volume, cumulated_quantity, inter_obj)
        expected_result = [{'date': '2022-01-01', 'volume': -200}, {'date': '2022-01-02', 'volume': 400}]
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()