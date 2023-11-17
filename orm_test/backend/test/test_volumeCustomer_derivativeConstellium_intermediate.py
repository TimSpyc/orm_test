import unittest
from unittest.mock import Mock, patch
from backend.src.intermediate import VolumeCustomerDerivativeConstelliumIntermediate


class TestVolumeCustomerDerivativeConstelliumIntermediate(VolumeCustomerDerivativeConstelliumIntermediate):

    def __new__(cls) -> object:
        return super().__new__(cls)
    def __init__(self):
        pass

class TestGetVolume(unittest.TestCase):
    @patch('backend.src.manager.customer_volume_manager.CustomerVolumeManager.filter', autospec=True)
    def test_simpleResult(self, mock_filter):
        # Mocking the dependencies
        volume_manager = Mock()
        volume_manager.current_volume = {'volume_date': '2022-01-01', 'volume': 100}
        mock_filter.return_value = [volume_manager]

        # Creating an instance of the class and setting the dependencies
        instance = TestVolumeCustomerDerivativeConstelliumIntermediate()
        instance.search_date = '2022-01-01'

        # Calling the function and checking the result
        result = instance.getVolume(1)
        self.assertEqual(result, {'volume_date': '2022-01-01', 'volume': 100})

    @patch('backend.src.manager.customer_volume_manager.CustomerVolumeManager.filter', autospec=True)
    def test_errorMessageEmptyVolumeManagerList(self, mock_filter):
        mock_filter.return_value = []

        instance = TestVolumeCustomerDerivativeConstelliumIntermediate()
        instance.search_date = '2022-01-01'

        with self.assertRaises(ValueError):
            instance.getVolume(1)

    @patch('backend.src.manager.customer_volume_manager.CustomerVolumeManager.filter', autospec=True)
    def test_errorMessageTwoVolumeManagerList(self, mock_filter):
        volume_manager_1 = Mock()
        volume_manager_1.current_volume = {'volume_date': '2022-01-01', 'volume': 100}
        volume_manager_2 = Mock()
        volume_manager_2.current_volume = {'volume_date': '2022-01-01', 'volume': 100}
        mock_filter.return_value = [volume_manager_1, volume_manager_2]

        instance = TestVolumeCustomerDerivativeConstelliumIntermediate()
        instance.search_date = '2022-01-01'

        with self.assertRaises(ValueError):
            instance.getVolume(1)

if __name__ == '__main__':
    unittest.main()