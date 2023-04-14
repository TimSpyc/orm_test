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

from backend.models import DerivativeConstelliumGroup, DerivativeConstellium, User
from datetime import datetime
from manager import GeneralManager
import timeit

class DerivativeConstelliumManager(GeneralManager):
    """
    A manager class for handling DerivativeConstellium-related operations, extending the GeneralManager.

    Attributes:
        group_model (models.Model): The DerivativeConstelliumGroup model.
        data_model (models.Model): The DerivativeConstellium model.
    """
    group_model = DerivativeConstelliumGroup
    data_model = DerivativeConstellium

    def __init__(self, derivative_constellium_group_id, search_date=None, use_cache=True):
        """
        Initialize a DerivativeConstelliumManager instance.

        Args:
            derivative_constellium_group_id (int): The ID of the DerivativeConstelliumGroup instance.
            search_date (datetime.datetime, optional): The date used for filtering data. Defaults to None.
            use_cache (bool, optional): Whether to use the cache for data retrieval. Defaults to True.
        """
        derivative_constellium_group, derivative_constellium = super().__init__(
            group_id=derivative_constellium_group_id,
            search_date=search_date
        )
        self.project_group_id = derivative_constellium_group.project_group.id
        self.name = derivative_constellium.name
        self.sop_date = derivative_constellium.sop_date
        self.eop_date = derivative_constellium.eop_date
        self.derivative_type_id = derivative_constellium.derivative_type.id
        self.derivative_type = derivative_constellium.derivative_type.name
        self.estimated_price = derivative_constellium.estimated_price
        self.estimated_weight = derivative_constellium.estimated_weight
        self.prediction_accuracy_id = derivative_constellium.prediction_accuracy.id
        self.prediction_accuracy = derivative_constellium.prediction_accuracy.name

    @property
    def project_manager(self):
        """
        Get a ProjectManager instance for the current DerivativeConstelliumManager.

        Returns:
            ProjectManager: An instance of the ProjectManager class.
        """
        from project_manager import ProjectManager
        return ProjectManager(self.project_group_id, self.search_date)
