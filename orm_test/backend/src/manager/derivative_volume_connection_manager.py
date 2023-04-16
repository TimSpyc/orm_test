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

from backend.models import DerivativeVolumeLMCDerivativeConstelliumConnectionGroup, DerivativeVolumeLMCDerivativeConstelliumConnection
from manager import GeneralManager


class DerivativeLMCDerivativeConstelliumConnectionManager(GeneralManager):
    group_model = DerivativeVolumeLMCDerivativeConstelliumConnectionGroup
    data_model = DerivativeVolumeLMCDerivativeConstelliumConnection

    def __init__(self, derivative_connection_group_id, search_date=None, use_cache=True):
        connection_group, connection = super().__init__(
            group_id=derivative_connection_group_id,
            search_date=search_date
        )
    
        self.take_rate = connection.take_rate