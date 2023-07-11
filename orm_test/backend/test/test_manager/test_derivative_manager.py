from backend.models import DerivativeConstellium, DerivativeConstelliumGroup, DerivativeType, FileGroup, Location, PredictionAccuracy, ProjectGroup, User
from django.test import TestCase
from backend.src.manager.derivative_constellium_manager import DerivativeConstelliumManager
import datetime


class DerivativeConstelliumManagerTest(TestCase):  

    def setUp(self):
        self.user = User.objects.create()
        self.group_id = 1 
        self.creator_user_id = self.user.id
        self.project_group = ProjectGroup.objects.create()
        self.derivative_constellium_group = DerivativeConstelliumGroup.objects.create(
            project_group = self.project_group)
        self.derivative_type = DerivativeType.objects.create(name='derivativeType')
        self.prediction_accuracy = PredictionAccuracy.objects.create(name='predictionAccuracy')
        self.file_group = FileGroup.objects.create(name ='fileGroup')
        self.location = Location.objects.create(name='location')
        kwargs = {
                'derivative_constellium_group': self.derivative_constellium_group,
                'name' : 'derivativeName',
                'sop_date': datetime.date.today(),
                'eop_date' : datetime.date.today(),
                'location' : self.location,
                'derivative_type' : self.derivative_type,
                'estimated_price' : 20.02,
                'estimated_weight' : 200,
                'prediction_accuracy' : self.prediction_accuracy,
                'file_group' : self.file_group,
                'project_group' : self.project_group
            }
        self.derivative_constellium_manager_obj = DerivativeConstelliumManager.create(self.creator_user_id, **kwargs)
        
    def test_create(self):
        kwargs = {
            'derivative_constellium_group': self.derivative_constellium_group,
            'name' : 'derivativeName',
            'sop_date': datetime.date.today(),
            'eop_date' : datetime.date.today(),
            'location' : self.location,
            'derivative_type' : self.derivative_type,
            'estimated_price' : 20.02,
            'estimated_weight' : 200,
            'prediction_accuracy' : self.prediction_accuracy,
            'file_group' : self.file_group,
            'project_group' : self.project_group
        }
        derivative_constellium_manager_obj= DerivativeConstelliumManager.create(self.creator_user_id, **kwargs)

        self.assertIsInstance(derivative_constellium_manager_obj, DerivativeConstelliumManager)
        
        obj = DerivativeConstellium.objects.get(id=derivative_constellium_manager_obj.id)
        self.assertEqual(obj.name, 'derivativeName')  
        self.assertEqual(obj.derivative_constellium_group.id, 3)
        self.assertEqual(obj.sop_date, derivative_constellium_manager_obj.sop_date)
        self.assertEqual(obj.eop_date, derivative_constellium_manager_obj.eop_date)
        self.assertEqual(obj.location, self.location)
        self.assertEqual(obj.derivative_type, self.derivative_type)
        self.assertEqual(obj.estimated_price, 20.02)
        self.assertEqual(obj.estimated_weight, 200)
        self.assertEqual(obj.prediction_accuracy, self.prediction_accuracy)
        self.assertEqual(obj.file_group.id, self.file_group.id)

    def test_update(self): 
        update = {
            'estimated_price': 21,
            'estimated_weight' : 300   
        }
        derivative_constellium_manager = DerivativeConstelliumManager(self.derivative_constellium_manager_obj.derivative_constellium_group)
        derivative_constellium_manager.update(self.creator_user_id, **update)

        updated_obj = DerivativeConstellium.objects.latest('id')
        self.assertEqual(updated_obj.estimated_price, 21)
        self.assertEqual(updated_obj.estimated_weight, 300)

    def test_deactivate(self):
        derivative_constellium_manager = DerivativeConstelliumManager(self.derivative_constellium_manager_obj.derivative_constellium_group)
        obj = DerivativeConstellium.objects.get(id = self.derivative_constellium_manager_obj.id)

        self.assertTrue(obj.active)
        derivative_constellium_manager.deactivate(self.creator_user_id)
        deactivated_obj = DerivativeConstellium.objects.latest('id')
        self.assertFalse(deactivated_obj.active)

    def test_filter(self):

        filter_kwargs = {
            'location' : self.location,
            'derivative_type' : self.derivative_type,
            'estimated_price' : 20.02,
        }
        result = DerivativeConstelliumManager.filter(**filter_kwargs)
        expected_result = [
            DerivativeConstelliumManager(derivative_constellium_group_id=self.derivative_constellium_manager_obj.derivative_constellium_group) 
        ]
        self.assertEqual(result, expected_result)   



