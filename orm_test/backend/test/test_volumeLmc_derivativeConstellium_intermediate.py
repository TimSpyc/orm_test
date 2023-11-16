import unittest
from unittest.mock import Mock, patch
from backend.src.intermediate import VolumeLmcDerivativeConstelliumIntermediate


class TestGetVolume(unittest.TestCase):
    @patch('volumeLmc_derivativeConstellium_intermediate.DerivativeLmcVolumeManager', autospec=True)
    def test_oneDerivativeLmcGroup(self, mock_derivative_lmc_volume_manager):
        # Mocking the dependencies
        derivative_lmc_group = Mock()
        derivative_lmc_group.id = 1

        extension_data = {'derivative_lmc_group': derivative_lmc_group, 'take_rate': 0.5}
        derivative_constellium_manager = Mock()
        derivative_constellium_manager.derivative_constellium_derivative_lmc_connection_dict_list = [extension_data]

        current_volume = [{'volume_date': '2022-01-01', 'volume': 100}, {'volume_date': '2022-01-02', 'volume': 200}]
        mock_derivative_lmc_volume_manager.return_value.current_volume = current_volume

        # Creating an instance of the class and setting the dependencies
        instance = VolumeLmcDerivativeConstelliumIntermediate()  # replace with your actual class name
        instance.derivative_constellium_manager = derivative_constellium_manager
        instance.search_date = '2022-01-01'

        # Calling the function and checking the result
        result = instance.getVolume()
        expected_result = [{'date': '2022-01-01', 'volume': 50.0}, {'date': '2022-01-02', 'volume': 100.0}]
        self.assertEqual(result, expected_result)

    @patch('volumeLmc_derivativeConstellium_intermediate.DerivativeLmcVolumeManager', autospec=True)
    def test_twoDerivativeLmcGroup(self, mock_derivative_lmc_volume_manager):
        # Mocking the dependencies
        derivative_lmc_group_1 = Mock()
        derivative_lmc_group_1.id = 1
        derivative_lmc_group_2 = Mock()
        derivative_lmc_group_2.id = 2

        extension_data_1 = {'derivative_lmc_group': derivative_lmc_group_1, 'take_rate': 0.5}
        extension_data_2 = {'derivative_lmc_group': derivative_lmc_group_2, 'take_rate': 0.25}
        derivative_constellium_manager = Mock()
        derivative_constellium_manager.derivative_constellium_derivative_lmc_connection_dict_list = [extension_data_1, extension_data_2]

        current_volume = [{'volume_date': '2022-01-01', 'volume': 100}, {'volume_date': '2022-01-02', 'volume': 200}]
        mock_derivative_lmc_volume_manager.return_value.current_volume = current_volume

        # Creating an instance of the class and setting the dependencies
        instance = VolumeLmcDerivativeConstelliumIntermediate()  # replace with your actual class name
        instance.derivative_constellium_manager = derivative_constellium_manager
        instance.search_date = '2022-01-01'

        # Calling the function and checking the result
        result = instance.getVolume()
        expected_result = [{'date': '2022-01-01', 'volume': 75.0}, {'date': '2022-01-02', 'volume': 150.0}]
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()