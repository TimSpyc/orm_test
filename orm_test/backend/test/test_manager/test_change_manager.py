from django.test import TestCase
from backend.models import ChangeRequest, ChangeRequestCost, ChangeRequestCostGroup, ChangeRequestFeasibility, ChangeRequestFeasibilityGroup, ChangeRequestGroup, ChangeRequestRisk, ChangeRequestRiskGroup, ChangeRequestRiskImpact, ChangeRequestRiskProbability, DerivativeConstelliumGroup, ProjectGroup, ProjectUserRole, User
from backend.src.manager.change_request_manager import ChangeRequestManager
from backend.src.manager.change_request_feasibility_manager import ChangeRequestFeasibilityManager
from backend.src.manager.change_request_risk_manager import ChangeRequestRiskManager
from backend.src.manager.change_request_cost_manager import ChangeRequestCostManager


class ChangeRequestRiskManagerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create()
        self.group_id = 1 
        self.creator_user_id = self.user.id
        self.project_user_role = ProjectUserRole.objects.create(name = 'role1')
        self.project_group = ProjectGroup.objects.create()

        self.change_request_group = ChangeRequestGroup.objects.create(
            project_group = self.project_group,
            change_request_no = 2
        )
        self.change_request_risk_group = ChangeRequestRiskGroup.objects.create(
            change_request_group = self.change_request_group,
            project_user_role = self.project_user_role
        )
        
        self.change_request_risk_probability = ChangeRequestRiskProbability.objects.create(
            name = 'nameRisk',
            factor = 0.4
            )
        self.change_request_risk_impact = ChangeRequestRiskImpact.objects.create(
            name = 'nameRiskImpact',
            factor = 0.3
            ) 
        
        kwargs = {
            'description': 'description1',
            'feedback' : 'feedback',
            'next_step': 'next_step',
            'change_request_risk_group': self.change_request_risk_group,
            'change_request_risk_probability': self.change_request_risk_probability,
            'change_request_risk_impact': self.change_request_risk_impact,
            'change_request_group': self.change_request_group,
            'project_user_role': self.project_user_role
            }
        self.change_request_risk_manager_obj = ChangeRequestRiskManager.create(self.creator_user_id, **kwargs)
        
    def test_create(self):
        kwargs = {
            'description': 'description1',
            'feedback' : 'feedback',
            'next_step': 'next_step',
            'change_request_risk_group': self.change_request_risk_group,
            'change_request_risk_probability': self.change_request_risk_probability,
            'change_request_risk_impact': self.change_request_risk_impact,
            'change_request_group': self.change_request_group,
            'project_user_role': self.project_user_role
        }
        change_request_risk_manager_obj = ChangeRequestRiskManager.create(self.creator_user_id, **kwargs)

        self.assertIsInstance(change_request_risk_manager_obj, ChangeRequestRiskManager)
        
        obj = ChangeRequestRisk.objects.get(id=change_request_risk_manager_obj.id)
        self.assertEqual(obj.description, 'description1')  
        self.assertEqual(obj.feedback, 'feedback')
        self.assertEqual(obj.next_step, 'next_step')
        self.assertEqual(obj.change_request_risk_group.id, 3)#NEW GROUP
        self.assertEqual(obj.change_request_risk_probability, self.change_request_risk_probability)
        self.assertEqual(obj.change_request_risk_impact, self.change_request_risk_impact)

    def test_update(self): 
        update = {
            'feedback': 'feedbackNew',
            'next_step' : 'next_stepNew'   
        }
        change_request_risk_manager = ChangeRequestRiskManager(self.change_request_risk_manager_obj.change_request_risk_group)
        change_request_risk_manager.update(self.creator_user_id, **update)

        updated_obj = ChangeRequestRisk.objects.latest('id')
        self.assertEqual(updated_obj.feedback, 'feedbackNew')
        self.assertEqual(updated_obj.next_step, 'next_stepNew')

    def test_deactivate(self):
        change_request_risk_manager = ChangeRequestRiskManager(self.change_request_risk_manager_obj.change_request_risk_group)
        obj = ChangeRequestRisk.objects.get(id = self.change_request_risk_manager_obj.id)

        self.assertTrue(obj.active)
        change_request_risk_manager.deactivate(self.creator_user_id)
        deactivated_obj = ChangeRequestRisk.objects.latest('id')
        self.assertFalse(deactivated_obj.active)

    def test_filter(self):
        filter_kwargs = {
            'next_step': 'next_step',
        }
        result = ChangeRequestRiskManager.filter(**filter_kwargs)
        expected_result = [
            ChangeRequestRiskManager(change_request_risk_group_id=self.change_request_risk_manager_obj.change_request_risk_group) 
        ]
        self.assertEqual(result, expected_result)  


class ChangeRequestManagerTest(TestCase):

    def setUp(self):
        self.user = User.objects.create()
        self.group_id = 1 
        self.creator_user_id = self.user.id
        self.project_group = ProjectGroup.objects.create()
        self.change_request_group = ChangeRequestGroup.objects.create(
            project_group = self.project_group,
            change_request_no = 2
        )
        self.derivative_constellium_group = DerivativeConstelliumGroup.objects.create(
            project_group = self.project_group
        )
        kwargs = {
                'customer_part_number': '11a',
                'customer_part_name' : 'customerName',
                'description': 'description1',
                'ECR_number': '123',
                'customer_approval': True,
                'internal_approval': False,
                'project_group' : self.change_request_group.project_group,
                'derivative_constellium_group' : self.derivative_constellium_group,
                'change_request_no' : self.change_request_group.change_request_no
           }
        self.change_request_manager_obj = ChangeRequestManager.create(self.creator_user_id, **kwargs)
        
    def test_create(self):
        kwargs = {
                'customer_part_number': '11a',
                'customer_part_name' : 'customerName',
                'description': 'description1',
                'ECR_number': '123',
                'customer_approval': True,
                'internal_approval': False,
                'project_group' : self.change_request_group.project_group,
                #'change_request_group' : self.change_request_group,
                'derivative_constellium_group' : self.derivative_constellium_group,
                'change_request_no' : self.change_request_group.change_request_no
            }
        change_request_manager_obj = ChangeRequestManager.create(self.creator_user_id, **kwargs)
        self.assertIsInstance(change_request_manager_obj, ChangeRequestManager)
        
        obj = ChangeRequest.objects.get(id=change_request_manager_obj.id) 

        self.assertEqual(obj.customer_part_number, '11a')
        self.assertEqual(obj.customer_part_name, 'customerName')
        self.assertEqual(obj.description, 'description1')
        self.assertEqual(obj.ECR_number, '123')
        self.assertTrue(obj.customer_approval)
        self.assertFalse(obj.internal_approval)
        self.assertEqual(obj.change_request_group.project_group, self.project_group)
        self.assertEqual(obj.derivative_constellium_group, self.derivative_constellium_group)
        self.assertEqual(obj.change_request_group.change_request_no, 2)
        self.assertEqual(obj.change_request_group.id, self.change_request_group.id)

    def test_update(self): 
        update = {
            'customer_part_number': '12b',
            'ECR_number' : 12345   
        }
        change_request_manager = ChangeRequestManager(self.change_request_manager_obj.change_request_group)
        change_request_manager.update(self.creator_user_id, **update)

        updated_obj = ChangeRequest.objects.latest('id')
        self.assertEqual(updated_obj.customer_part_number, '12b')
        self.assertEqual(updated_obj.ECR_number, '12345')

    def test_deactivate(self):
        change_request_manager = ChangeRequestManager(self.change_request_manager_obj.change_request_group)
        obj = ChangeRequest.objects.get(id = self.change_request_manager_obj.id)

        self.assertTrue(obj.active)
        change_request_manager.deactivate(self.creator_user_id)
        deactivated_obj = ChangeRequest.objects.latest('id')
        self.assertFalse(deactivated_obj.active)

    def test_filter(self):
        filter_kwargs = {
            'customer_part_name' : 'customerName',
            'derivative_constellium_group' : self.derivative_constellium_group,
        }
        result = ChangeRequestManager.filter(**filter_kwargs)
        expected_result = [
            ChangeRequestManager(change_request_group_id=self.change_request_manager_obj.change_request_group) 
        ]
        self.assertEqual(result, expected_result)  


class ChangeRequestFeasibilityManagerTest(TestCase):

    def setUp(self):
        self.user = User.objects.create()
        self.group_id = 1 
        self.creator_user_id = self.user.id
        self.project_group = ProjectGroup.objects.create()
        self.project_user_role = ProjectUserRole.objects.create(name = 'role1')
        self.change_request_group = ChangeRequestGroup.objects.create(
            project_group = self.project_group,
            change_request_no = 2
        )
        self.change_request_feasibility_group = ChangeRequestFeasibilityGroup.objects.create(
            change_request_group = self.change_request_group,
            project_user_role = self.project_user_role
        )
        kwargs = {
                'confirmed' : True,
                'description': 'description1',
                'change_request_group': self.change_request_group,
                'project_user_role': self.project_user_role
           }
        self.change_request_feasibility_manager_obj = ChangeRequestFeasibilityManager.create(self.creator_user_id, **kwargs)
        
    def test_create(self):
        kwargs = {
                #'change_request_feasibility_group': self.change_request_feasibility_group,
                'confirmed' : True,
                'description': 'description1',
                'change_request_group': self.change_request_group,
                'project_user_role': self.project_user_role
           }
        change_request_feasibility_manager_obj = ChangeRequestFeasibilityManager.create(self.creator_user_id, **kwargs)
        self.assertIsInstance(change_request_feasibility_manager_obj, ChangeRequestFeasibilityManager)
        
        obj = ChangeRequestFeasibility.objects.get(id=change_request_feasibility_manager_obj.id) 

        self.assertEqual(obj.change_request_feasibility_group, self.change_request_feasibility_group)
        self.assertTrue(obj.confirmed)
        self.assertEqual(obj.description, 'description1')
        self.assertEqual(obj.change_request_feasibility_group.id, self.change_request_feasibility_group.id)# keine group2 gleiche genutzt weil unique in groupTable

    def test_update(self): 
        update = {
           'confirmed' : False,
        }
        change_request_feasibility_manager = ChangeRequestFeasibilityManager(self.change_request_feasibility_manager_obj.change_request_feasibility_group)
        change_request_feasibility_manager.update(self.creator_user_id, **update)

        updated_obj = ChangeRequestFeasibility.objects.latest('id')
        self.assertFalse(updated_obj.confirmed)

    def test_deactivate(self):
        change_request_feasibility_manager = ChangeRequestFeasibilityManager(self.change_request_feasibility_manager_obj.change_request_feasibility_group)
        obj = ChangeRequestFeasibility.objects.get(id = self.change_request_feasibility_manager_obj.id)

        self.assertTrue(obj.active)
        change_request_feasibility_manager.deactivate(self.creator_user_id)
        deactivated_obj = ChangeRequestFeasibility.objects.latest('id')
        self.assertFalse(deactivated_obj.active)

    def test_filter(self):
        filter_kwargs = {
            'confirmed' : True,
            'description': 'description1',
        }
        result = ChangeRequestFeasibilityManager.filter(**filter_kwargs)
        expected_result = [
            ChangeRequestFeasibilityManager(change_request_feasibility_group_id=self.change_request_feasibility_manager_obj.change_request_feasibility_group) 
        ]
        self.assertEqual(result, expected_result)  


class ChangeRequestCostManagerTest(TestCase):

    def setUp(self):
        self.user = User.objects.create()
        self.group_id = 1 
        self.creator_user_id = self.user.id
        self.project_group = ProjectGroup.objects.create()
        self.project_user_role = ProjectUserRole.objects.create(name = 'role1')

        self.change_request_group = ChangeRequestGroup.objects.create(
            project_group = self.project_group,
            change_request_no = 2
        )
        self.change_request_cost_group = ChangeRequestCostGroup.objects.create(
            change_request_group = self.change_request_group,
            project_user_role = self.project_user_role
        )
        kwargs = {
                'change_request_cost_group': self.change_request_cost_group,
                'description': 'description1',
                'cost_estimation': 123000,
                'project_user_role' : self.project_user_role,
                'change_request_group': self.change_request_group
           }
        self.change_request_cost_manager_obj = ChangeRequestCostManager.create(self.creator_user_id, **kwargs)
        
    def test_create(self):
        kwargs = {
                'change_request_cost_group': self.change_request_cost_group,
                'description': 'description1',
                'cost_estimation': 123000,
                'project_user_role' : self.project_user_role,
                'change_request_group': self.change_request_group
           }
        change_request_cost_manager_obj = ChangeRequestCostManager.create(self.creator_user_id, **kwargs)
        self.assertIsInstance(change_request_cost_manager_obj, ChangeRequestCostManager)
        
        obj = ChangeRequestCost.objects.get(id=change_request_cost_manager_obj.id) 

        self.assertEqual(obj.cost_estimation, 123000)
        self.assertEqual(obj.change_request_cost_group, self.change_request_cost_group)
        self.assertEqual(obj.description, 'description1')
        self.assertEqual(obj.change_request_cost_group.change_request_group.id, self.change_request_cost_group.id)
        self.assertEqual(obj.change_request_cost_group.project_user_role.id, self.project_user_role.id)
        self.assertEqual(obj.change_request_cost_group.id, self.change_request_cost_group.id)


    def test_update(self): 
        update = {
            'cost_estimation' : 23000   
        }
        change_request_cost_manager = ChangeRequestCostManager(self.change_request_cost_manager_obj.change_request_cost_group)
        change_request_cost_manager.update(self.creator_user_id, **update)

        updated_obj = ChangeRequestCost.objects.latest('id')
        self.assertEqual(updated_obj.cost_estimation, 23000)

    def test_deactivate(self):
        change_request_cost_manager = ChangeRequestCostManager(self.change_request_cost_manager_obj.change_request_cost_group)
        obj = ChangeRequestCost.objects.get(id = self.change_request_cost_manager_obj.id)

        self.assertTrue(obj.active)
        change_request_cost_manager.deactivate(self.creator_user_id)
        deactivated_obj = ChangeRequestCost.objects.latest('id')
        self.assertFalse(deactivated_obj.active)

    def test_filter(self):
        filter_kwargs = {
                'description': 'description1',
        }
        result = ChangeRequestCostManager.filter(**filter_kwargs)
        expected_result = [
            ChangeRequestCostManager(change_request_cost_group_id=self.change_request_cost_manager_obj.change_request_cost_group) 
        ]
        self.assertEqual(result, expected_result)  