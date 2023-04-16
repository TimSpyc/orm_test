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

from backend.src.manager.derivative_constellium_manager import DerivativeConstelliumManager
from backend.src.manager.derivative_lmc_manager import DerivativeLmcManager
from backend.src.manager.derivative_constellium_manager import DerivativeLMCDerivativeConstelliumConnectionManager
from backend.src.manager.derivative_volume_manager import DerivativeLmcVolumeManager


# cache:
# search_date
# manager dependency group_ids
# intermediate dependency group_ids
# 

class DerivativeConstelliumVolume:
    manager_dependencies = [
        DerivativeConstelliumManager,
        DerivativeLmcManager,
        DerivativeLMCDerivativeConstelliumConnectionManager,
        DerivativeLmcVolumeManager
    ]
    intermediate_dependencies = []

    def __init__(self, derivative_constellium_group_id, search_date=None, use_cache=None):
        
        self._volume_lmc = None
    
    @property
    def volume_lmc(self):
        if _volume_lmc is None:
            pass

        return _volume_lmc

    def __volume_details(self):
