if __name__ == '__main__':
    import sys
    import os

    sys.path.append(r'C:\Users\Spyc\Django_ORM')
    sys.path.append(r'C:\Users\Spyc\Django_ORM\orm_test')
    sys.path.append(r'C:\Users\Spyc\Django_ORM\orm_test\orm_test')
    sys.path.append(r'C:\Users\Spyc\Django_ORM\orm_test\backend\src\manager')
    sys.path.append(r'C:\Users\Spyc\Django_ORM\orm_test\backend\src\auxiliary')
    sys.path.append(r'C:\Users\Spyc\Django_ORM\orm_test\backend')
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'orm_test.settings')

    import django
    django.setup()

from backend.models import DerivativeVolumeGroupLMC, DerivativeVolumeLMC
from manager import GeneralManager

class DerivativeLmcVolumeManager(GeneralManager):
    group_model = DerivativeVolumeGroupLMC
    data_model = DerivativeVolumeLMC

    def __init__(self, derivative_volume_group_id, search_date=None, use_cache=True):
        derivative_volume_group, derivative_volume = super().__init__(
            group_id=derivative_volume_group_id,
            search_date=search_date
        )

        self.derivative_group = derivative_volume.volume_group.derivative_group
        self.year = derivative_volume.volume_group.year
        self.month = derivative_volume.volume_group.month
        self.lmc_revision = derivative_volume.lmc_revision
        self.volume = derivative_volume.volume

    @property
    def derivative_list(self):
        from derivative_lmc_manager import DerivativeLmcManager
        return DerivativeLmcManager.filter(
            date=self.search_date,
            derivative_group_id=self.group_id
        )