from datetime import date
from backend.models.reference_models import RevisionLMC
from backend.src.manager.derivative_lmc_manager import DerivativeLmcGroup, DerivativeLmcVolumeManager
from django.test import TestCase


class TestGetVolumeForLmcRev(TestCase):
    def setUp(self):

        self.derivative_lmc_group= DerivativeLmcGroup.objects.create(
            lmc_full_code = '12345',
            lmc_model_code = '67890'
        )
        self.manager = DerivativeLmcVolumeManager.__new__(DerivativeLmcVolumeManager)
        self.test_revision = RevisionLMC.objects.create(revision_date=date(2023, 8, 29))
        self.manager.derivative_lmc_group_id = self.derivative_lmc_group.id

        self.manager.search_date = date(2023, 8, 29)


    # def test_get_volume_for_lmc_rev(self):
    #     result = self.manager.getVolumeForLmcRev(date(2023, 8, 29))
    #     expected_result = [{'volume': 42, 'date': date(2023, 8, 29)}] 
    #     self.assertEqual(result, expected_result)