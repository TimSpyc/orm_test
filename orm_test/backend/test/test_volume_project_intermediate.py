import unittest
from unittest.mock import MagicMock
from backend.src.intermediate import (
    VolumeProjectIntermediate,
    VolumeLmcDerivativeConstelliumIntermediate,
    VolumeCustomerDerivativeConstelliumIntermediate
)
import datetime


class TestVolumeLmcProjectIntermediate(VolumeProjectIntermediate):

    def __new__(cls) -> object:
        return super().__new__(cls)
    def __init__(self):
        pass


class TestGetVolumeWithVolumeLmcDerivativeConstelliumIntermediate(unittest.TestCase):
    def test_validVolumeWithSameDates(self):
        # Create a mock VolumeDerivativeConstelliumIntermediate object
        inter_obj = MagicMock()
        inter_obj.volume = [
            {'date': datetime.date(2022, 1, 1), 'volume': 100},
            {'date': datetime.date(2021, 1, 1), 'volume': 200},
            {'date': datetime.date(2020, 1, 1), 'volume': 300}
        ]

        VolumeLmcDerivativeConstelliumIntermediate.__new__ = MagicMock(return_value=inter_obj)

        # Create a VolumeLmcProjectIntermediate object and call the getVolume method
        intermediate = TestVolumeLmcProjectIntermediate()
        intermediate.VolumeDerivativeIntermediateClass = VolumeLmcDerivativeConstelliumIntermediate
        intermediate.search_date = datetime.date(2022, 1, 1)
        intermediate.derivative_constellium_group_dict_list = [{
            'id': 1
        }, {
            'id': 2
        }, {
            'id': 3
        }]
        result = intermediate.getVolume()

        # Check that the result is a list of dictionaries with the expected keys and values
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0]['date'], datetime.date(2022, 1, 1))
        self.assertEqual(result[0]['volume'], 300)
        self.assertEqual(result[1]['date'], datetime.date(2021, 1, 1))
        self.assertEqual(result[1]['volume'], 600)
        self.assertEqual(result[2]['date'], datetime.date(2020, 1, 1))
        self.assertEqual(result[2]['volume'], 900)
        
    def test_emptyVolumeList(self):
        inter_obj = MagicMock()
        inter_obj.volume = []

        VolumeLmcDerivativeConstelliumIntermediate.__new__ = MagicMock(return_value=inter_obj)

        intermediate = TestVolumeLmcProjectIntermediate()
        intermediate.VolumeDerivativeIntermediateClass = VolumeLmcDerivativeConstelliumIntermediate
        intermediate.search_date = datetime.date(2022, 1, 1)
        intermediate.derivative_constellium_group_dict_list = [{
            'id': 1
        }, {
            'id': 2
        }, {
            'id': 3
        }]
        result = intermediate.getVolume()

        self.assertEqual(len(result), 0)
        with self.assertRaises(IndexError):
            result[0]['date']
        with self.assertRaises(IndexError):
            result[0]['volume']

    def test_partlyEmptyVolumeList(self):
        inter_obj = MagicMock()
        inter_obj.volume = [
            {'date': datetime.date(2022, 1, 1), 'volume': 100},
            {'date': datetime.date(2021, 1, 1), 'volume': 0},
            {'date': datetime.date(2020, 1, 1), 'volume': 0.25}
        ]

        VolumeLmcDerivativeConstelliumIntermediate.__new__ = MagicMock(return_value=inter_obj)

        intermediate = TestVolumeLmcProjectIntermediate()
        intermediate.VolumeDerivativeIntermediateClass = VolumeLmcDerivativeConstelliumIntermediate
        intermediate.search_date = datetime.date(2022, 1, 1)
        intermediate.derivative_constellium_group_dict_list = [{
            'id': 1
        }, {
            'id': 2
        }]
        result = intermediate.getVolume()

        self.assertEqual(len(result), 3)
        self.assertEqual(result[0]['date'], datetime.date(2022, 1, 1))
        self.assertEqual(result[0]['volume'], 200)
        self.assertEqual(result[1]['date'], datetime.date(2021, 1, 1))
        self.assertEqual(result[1]['volume'], 0)
        self.assertEqual(result[2]['date'], datetime.date(2020, 1, 1))
        self.assertEqual(result[2]['volume'], 0.5)

class TestGetVolumeWithVolumeCustomerDerivativeConstelliumIntermediate(unittest.TestCase):
    def test_validVolumeWithSameDates(self):
        # Create a mock VolumeDerivativeConstelliumIntermediate object
        inter_obj = MagicMock()
        inter_obj.volume = [
            {'date': datetime.date(2022, 1, 1), 'volume': 100},
            {'date': datetime.date(2021, 1, 1), 'volume': 200},
            {'date': datetime.date(2020, 1, 1), 'volume': 300}
        ]

        VolumeCustomerDerivativeConstelliumIntermediate.__new__ = MagicMock(return_value=inter_obj)

        # Create a VolumeLmcProjectIntermediate object and call the getVolume method
        intermediate = TestVolumeLmcProjectIntermediate()
        intermediate.VolumeDerivativeIntermediateClass = VolumeCustomerDerivativeConstelliumIntermediate
        intermediate.search_date = datetime.date(2022, 1, 1)
        intermediate.derivative_constellium_group_dict_list = [{
            'id': 1
        }, {
            'id': 2
        }, {
            'id': 3
        }]
        result = intermediate.getVolume()

        # Check that the result is a list of dictionaries with the expected keys and values
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0]['date'], datetime.date(2022, 1, 1))
        self.assertEqual(result[0]['volume'], 300)
        self.assertEqual(result[1]['date'], datetime.date(2021, 1, 1))
        self.assertEqual(result[1]['volume'], 600)
        self.assertEqual(result[2]['date'], datetime.date(2020, 1, 1))
        self.assertEqual(result[2]['volume'], 900)
        
    def test_emptyVolumeList(self):
        inter_obj = MagicMock()
        inter_obj.volume = []

        VolumeCustomerDerivativeConstelliumIntermediate.__new__ = MagicMock(return_value=inter_obj)

        intermediate = TestVolumeLmcProjectIntermediate()
        intermediate.VolumeDerivativeIntermediateClass = VolumeCustomerDerivativeConstelliumIntermediate
        intermediate.search_date = datetime.date(2022, 1, 1)
        intermediate.derivative_constellium_group_dict_list = [{
            'id': 1
        }, {
            'id': 2
        }, {
            'id': 3
        }]
        result = intermediate.getVolume()

        self.assertEqual(len(result), 0)
        with self.assertRaises(IndexError):
            result[0]['date']
        with self.assertRaises(IndexError):
            result[0]['volume']

    def test_partlyEmptyVolumeList(self):
        inter_obj = MagicMock()
        inter_obj.volume = [
            {'date': datetime.date(2022, 1, 1), 'volume': 100},
            {'date': datetime.date(2021, 1, 1), 'volume': 0},
            {'date': datetime.date(2020, 1, 1), 'volume': 0.25}
        ]

        VolumeCustomerDerivativeConstelliumIntermediate.__new__ = MagicMock(return_value=inter_obj)

        intermediate = TestVolumeLmcProjectIntermediate()
        intermediate.VolumeDerivativeIntermediateClass = VolumeCustomerDerivativeConstelliumIntermediate
        intermediate.search_date = datetime.date(2022, 1, 1)
        intermediate.derivative_constellium_group_dict_list = [{
            'id': 1
        }, {
            'id': 2
        }]
        result = intermediate.getVolume()

        self.assertEqual(len(result), 3)
        self.assertEqual(result[0]['date'], datetime.date(2022, 1, 1))
        self.assertEqual(result[0]['volume'], 200)
        self.assertEqual(result[1]['date'], datetime.date(2021, 1, 1))
        self.assertEqual(result[1]['volume'], 0)
        self.assertEqual(result[2]['date'], datetime.date(2020, 1, 1))
        self.assertEqual(result[2]['volume'], 0.5)