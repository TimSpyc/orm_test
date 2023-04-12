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

class DerivativeConstelliumManager(GeneralManager):
    group_model = DerivativeConstelliumGroup
    data_model = DerivativeConstellium

    def __init__(self, derivative_constellium_group_id, date=None, use_cache=True):
        derivative_constellium_group, derivative_constellium = super().__init__(
            group_id=derivative_constellium_group_id,
            date=date,
            use_cache=use_cache
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
        from project_manager import ProjectManager
        if self._project_manager is None:
            self._project_manager = ProjectManager(self.project_group_id, self.search_date)
        return self._project_manager

    @classmethod
    @createCache
    def create(cls, project_group_id, name, sop_date, eop_date, derivative_type_id, estimated_price, estimated_weight, prediction_accuracy_id, creator_user_id):
        derivative_constellium_group = DerivativeConstelliumGroup(
            project_group_id=project_group_id
        )
        derivative_constellium_group.save()

        new_derivative_constellium = DerivativeConstellium(
            derivative_constellium_group=derivative_constellium_group,
            name=name,
            sop_date=sop_date,
            eop_date=eop_date,
            derivative_type=DerivativeType.objects.get(id=derivative_type_id),
            estimated_price=estimated_price,
            estimated_weight=estimated_weight,
            prediction_accuracy=PredictionAccuracy.objects.get(id=prediction_accuracy_id),
            date=datetime.now(),
            creator=User.objects.get(id=creator_user_id),
            active=True
        )
        new_derivative_constellium.save()

        derivative_constellium_manager = cls(derivative_constellium_group.id)

        return derivative_constellium_manager

    @updateCache
    def update(self, creator_user_id, **kwargs):
        current_attributes = {
            'derivative_constellium_group': self.derivative_constellium_group,
            'name': self.name,
            'sop_date': self.sop_date,
            'eop_date': self.eop_date,
            'derivative_type': self.derivative_type,
            'estimated_price': self.estimated_price,
            'estimated_weight': self.estimated_weight,
            'prediction_accuracy': self.prediction_accuracy,
            'date': datetime.now(),
            'creator': User.objects.get(id=creator_user_id),
            'active': True
        }

        for key, value in kwargs.items():
            if key in current_attributes:
                current_attributes[key] = value
            else:
                raise ValueError(f"Invalid key: {key}")

        updated_derivative_constellium = DerivativeConstellium(**current_attributes)
        updated_derivative_constellium.save()

        self.__dict__.update(current_attributes)
        self.creator_user_id = creator_user_id

    @updateCache
    def deactivate(self):
        last_derivative_constellium = DerivativeConstellium.objects.get(id=self.id)

        deactivated_derivative_constellium = DerivativeConstellium(
            derivative_constellium_group_id=last_derivative_constellium.derivative_constellium_group_id,
            name=last_derivative_constellium.name,
            sop_date=last_derivative_constellium.sop_date,
            eop_date=last_derivative_constellium.eop_date,
            derivative_type=last_derivative_constellium.derivative_type,
            estimated_price=last_derivative_constellium.estimated_price,
            estimated_weight=last_derivative_constellium.estimated_weight,
            prediction_accuracy=last_derivative_constellium.prediction_accuracy,
            date=datetime.now(),
            creator=last_derivative_constellium.creator,
            active=False
        )

        deactivated_derivative_constellium.save()
