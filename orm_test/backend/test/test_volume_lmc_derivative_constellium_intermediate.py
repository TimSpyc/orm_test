from django.test import TestCase
from unittest.mock import MagicMock
from backend.models import DerivativeLmcVolume, DerivativeLmcGroup, RevisionLMC
import datetime
from backend.src.intermediate import VolumeLmcDerivativeConstelliumIntermediate

class Nothing:
    pass
class TestVolumeLmcDerivativeConstelliumIntermediate(VolumeLmcDerivativeConstelliumIntermediate):

    def __new__(cls) -> object:
        return super().__new__(cls)
    def __init__(self):
        pass


# class TestGetVolume(TestCase):
#     def setUp(self) -> None:

#         self.derivative_constellium_manager = Nothing()
#         self.object_with_id_1 = Nothing()
#         self.object_with_id_1.id = 1
#         self.object_with_id_2 = Nothing()
#         self.object_with_id_2.id = 2
#         self.object_with_id_3 = Nothing()
#         self.object_with_id_3.id = 3
#         self.object_with_id_4 = Nothing()
#         self.object_with_id_4.id = 4
        
#         revision_obj = RevisionLMC(
#             revision_date = datetime.date(2020, 1, 1),
#         )
#         revision_obj.save()
        
#         for i in range(10):
#             group_obj = DerivativeLmcGroup(
#                 lmc_full_code = f'test{i}',
#                 lmc_model_code = f'test{i}',
#             )
#             group_obj.save()
#             for year in range(10):
#                 volume_obj = DerivativeLmcVolume(
#                     derivative_lmc_group= group_obj,
#                     volume = 10,
#                     volume_date = datetime.date(2020+year, 1, 1),
#                     lmc_revision = revision_obj,
#                 )
#                 volume_obj.save()

#     def test_get_volume_with_one_derivative_lmc_and_takerate_1(self):
        
#         self.derivative_constellium_manager.derivative_constellium_derivative_lmc_connection_dict_list = [
#             {
#                 'derivative_lmc_group': self.object_with_id_1,
#                 'take_rate': 1
#             },
#         ]
        
#         intermediate = TestVolumeLmcDerivativeConstelliumIntermediate()
#         intermediate.derivative_constellium_manager = self.derivative_constellium_manager
#         intermediate.search_date = None
#         total_volume = intermediate.getVolume()
#         expected_total_volume = [
#             {'volume_date': datetime.date(2020, 1, 1), 'volume': 10},
#             {'volume_date': datetime.date(2021, 1, 1), 'volume': 10},
#             {'volume_date': datetime.date(2022, 1, 1), 'volume': 10},
#             {'volume_date': datetime.date(2023, 1, 1), 'volume': 10},
#             {'volume_date': datetime.date(2024, 1, 1), 'volume': 10},
#             {'volume_date': datetime.date(2025, 1, 1), 'volume': 10},
#             {'volume_date': datetime.date(2026, 1, 1), 'volume': 10},
#             {'volume_date': datetime.date(2027, 1, 1), 'volume': 10},
#             {'volume_date': datetime.date(2028, 1, 1), 'volume': 10},
#             {'volume_date': datetime.date(2029, 1, 1), 'volume': 10}
#         ]
#         self.assertEqual(total_volume, expected_total_volume)

#     def test_get_volume_with_one_derivative_lmc_and_takerate_025(self):
        
#         self.derivative_constellium_manager.derivative_constellium_derivative_lmc_connection_dict_list = [
#             {
#                 'derivative_lmc_group': self.object_with_id_1,
#                 'take_rate': 0.25
#             },
#         ]
        
#         intermediate = TestVolumeLmcDerivativeConstelliumIntermediate()
#         intermediate.derivative_constellium_manager = self.derivative_constellium_manager
#         intermediate.search_date = None
#         total_volume = intermediate.getVolume()
#         expected_total_volume = [
#             {'volume_date': datetime.date(2020, 1, 1), 'volume': 2.5},
#             {'volume_date': datetime.date(2021, 1, 1), 'volume': 2.5},
#             {'volume_date': datetime.date(2022, 1, 1), 'volume': 2.5},
#             {'volume_date': datetime.date(2023, 1, 1), 'volume': 2.5},
#             {'volume_date': datetime.date(2024, 1, 1), 'volume': 2.5},
#             {'volume_date': datetime.date(2025, 1, 1), 'volume': 2.5},
#             {'volume_date': datetime.date(2026, 1, 1), 'volume': 2.5},
#             {'volume_date': datetime.date(2027, 1, 1), 'volume': 2.5},
#             {'volume_date': datetime.date(2028, 1, 1), 'volume': 2.5},
#             {'volume_date': datetime.date(2029, 1, 1), 'volume': 2.5}
#         ]
#         self.assertEqual(total_volume, expected_total_volume)
        
#     def test_get_volume_with_multiple_derivative_lmc_and_different_takerate(self):
        
#         self.derivative_constellium_manager.derivative_constellium_derivative_lmc_connection_dict_list = [
#             {
#                 'derivative_lmc_group': self.object_with_id_1,
#                 'take_rate': 1
#             },
#             {
#                 'derivative_lmc_group': self.object_with_id_2,
#                 'take_rate': 0.5
#             },
#             {
#                 'derivative_lmc_group': self.object_with_id_3,
#                 'take_rate': 0.25
#             },
#             {
#                 'derivative_lmc_group': self.object_with_id_4,
#                 'take_rate': 2
#             },

#         ]
        
#         intermediate = TestVolumeLmcDerivativeConstelliumIntermediate()
#         intermediate.derivative_constellium_manager = self.derivative_constellium_manager
#         intermediate.search_date = None
#         total_volume = intermediate.getVolume()
#         expected_total_volume = [
#             {'volume_date': datetime.date(2020, 1, 1), 'volume': 37.5},
#             {'volume_date': datetime.date(2021, 1, 1), 'volume': 37.5},
#             {'volume_date': datetime.date(2022, 1, 1), 'volume': 37.5},
#             {'volume_date': datetime.date(2023, 1, 1), 'volume': 37.5},
#             {'volume_date': datetime.date(2024, 1, 1), 'volume': 37.5},
#             {'volume_date': datetime.date(2025, 1, 1), 'volume': 37.5},
#             {'volume_date': datetime.date(2026, 1, 1), 'volume': 37.5},
#             {'volume_date': datetime.date(2027, 1, 1), 'volume': 37.5},
#             {'volume_date': datetime.date(2028, 1, 1), 'volume': 37.5},
#             {'volume_date': datetime.date(2029, 1, 1), 'volume': 37.5}
#         ]
#         self.assertEqual(total_volume, expected_total_volume)

class TestGetVolumeV2(TestCase):
    def test_get_volume_with_one_derivative_lmc_and_takerate_1(self):
        #TODO Help
        der_lmc_volume = MagicMock()
        der_lmc_volume.current_volume = [
            {'volume_date': datetime.date(2022, 1, 1), 'volume': 100},
            {'volume_date': datetime.date(2021, 1, 1), 'volume': 200},
            {'volume_date': datetime.date(2020, 1, 1), 'volume': 300}
        ]
        
        DerivativeLmcVolume.__new__ = MagicMock(return_value=der_lmc_volume)

        derivative_lmc_group_object = MagicMock()
        derivative_lmc_group_object.id = 1
        
        intermediate = TestVolumeLmcDerivativeConstelliumIntermediate()
        intermediate.search_date = datetime.date(2022, 1, 1)
        intermediate.derivative_constellium_manager = MagicMock()
        intermediate.derivative_constellium_manager.\
            derivative_constellium_derivative_lmc_connection_dict_list = [
                {
                    'derivative_lmc_group': derivative_lmc_group_object,
                    'take_rate': 1
                },
            ]
        result = intermediate.getVolume()

        self.assertEqual(len(result), 3)
        self.assertEqual(result[0]['volume_date'], datetime.date(2022, 1, 1))
        self.assertEqual(result[0]['volume'], 300)
        self.assertEqual(result[1]['volume_date'], datetime.date(2021, 1, 1))
        self.assertEqual(result[1]['volume'], 600)
        self.assertEqual(result[2]['volume_date'], datetime.date(2020, 1, 1))
        self.assertEqual(result[2]['volume'], 900)