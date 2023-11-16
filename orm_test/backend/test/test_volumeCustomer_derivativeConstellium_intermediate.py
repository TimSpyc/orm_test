import unittest
from unittest.mock import Mock, patch
from backend.src.intermediate import VolumeCustomerDerivativeConstelliumIntermediate


class TestGetVolume(unittest.TestCase):
    @patch('volumeCustomer_derivativeConstellium_intermediate.CustomerVolumeManager.filter', autospec=True)
    def test_simpleResult(self, mock_filter):
        # Mocking the dependencies
        volume_manager = Mock()
        volume_manager.current_volume = {'volume_date': '2022-01-01', 'volume': 100}
        mock_filter.return_value = [volume_manager]

        # Creating an instance of the class and setting the dependencies
        instance = VolumeCustomerDerivativeConstelliumIntermediate()
        instance.search_date = '2022-01-01'

        # Calling the function and checking the result
        result = instance.getVolume(1)
        self.assertEqual(result, {'volume_date': '2022-01-01', 'volume': 100})

    @patch('volumeCustomer_derivativeConstellium_intermediate.CustomerVolumeManager.filter', autospec=True)
    def test_errorMessageEmptyVolumeManagerList(self, mock_filter):
        # Mocking the dependencies
        mock_filter.return_value = []

        # Creating an instance of the class and setting the dependencies
        instance = VolumeCustomerDerivativeConstelliumIntermediate()
        instance.search_date = '2022-01-01'

        # Calling the function and checking if it raises a ValueError
        with self.assertRaises(ValueError):
            instance.getVolume(1)

    @patch('volumeCustomer_derivativeConstellium_intermediate.CustomerVolumeManager.filter', autospec=True)
    def test_errorMessageTwoVolumeManagerList(self, mock_filter):
        # Mocking the dependencies
        volume_manager_1 = Mock()
        volume_manager_1.current_volume = {'volume_date': '2022-01-01', 'volume': 100}
        volume_manager_2 = Mock()
        volume_manager_2.current_volume = {'volume_date': '2022-01-01', 'volume': 100}
        mock_filter.return_value = [volume_manager_1, volume_manager_2]

        # Creating an instance of the class and setting the dependencies
        instance = VolumeCustomerDerivativeConstelliumIntermediate()
        instance.search_date = '2022-01-01'

        # Calling the function and checking if it raises a ValueError
        with self.assertRaises(ValueError):
            instance.getVolume(1)

if __name__ == '__main__':
    unittest.main()