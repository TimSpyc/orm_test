import unittest
import datetime
from backend.src.intermediate import intermediate_auxiliary

class TestCalculateShipment():
    pass

class TestAddListOfDictionaries(unittest.TestCase):
    
    def test_addListOfDictionaries(self):
        list_1 = [
            {
                'date': datetime.date(2022, 1, 1),
                'gross_weight': 100,
                'net_weight': 200,
                'other_net_weight': 300
            },
            {
                'date': datetime.date(2021, 1, 1),
                'gross_weight': 400,
                'net_weight': 500,
                'other_net_weight': 600
            },
            {
                'date': datetime.date(2020, 1, 1),
                'gross_weight': 700,
                'net_weight': 800,
                'other_net_weight': 900,
                'steel_gross_weight': 1000,
            }
            
        ]

        list_2 = [
            {
                'date': datetime.date(2022, 1, 1),
                'gross_weight': 100,
            },
            {
                'date': datetime.date(2021, 1, 1),
                'gross_weight': 400,
                'net_weight': 500,
                'steel_gross_weight': 600
            },
            {
                'date': datetime.date(2019, 1, 1),
                'gross_weight': 700,
                'net_weight': 800,
                'other_net_weight': 900,
                'steel_gross_weight': 1000,
            }
        ]
        
        expected_result = [
            {
                'date': datetime.date(2022, 1, 1),
                'gross_weight': 200,
                'net_weight': 400,
                'other_net_weight': 600
            },
            {
                'date': datetime.date(2021, 1, 1),
                'gross_weight': 800,
                'net_weight': 1000,
                'other_net_weight': 1200,
                'steel_gross_weight': 600,
            },
            {
                'date': datetime.date(2020, 1, 1),
                'gross_weight': 1400,
                'net_weight': 1600,
                'other_net_weight': 1800,
                'steel_gross_weight': 2000,
            },
            {
                'date': datetime.date(2019, 1, 1),
                'gross_weight': 700,
                'net_weight': 800,
                'other_net_weight': 900,
                'steel_gross_weight': 1000,
            }
        ]

        self.assertEqual(
            intermediate_auxiliary.AddListOfDictionaries(list_1, list_2),
            expected_result
        )