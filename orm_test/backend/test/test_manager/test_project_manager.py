import datetime
from django.test import TestCase
from backend.models import Currency, Customer, FileGroup, Project, ProjectGroup, ProjectNumber, ProjectStaffCost, ProjectStaffCostTask, ProjectStaffCostGroup, ProjectStatus, ProjectType, ProjectUser, ProjectUserGroup, ProjectUserRole, User
from backend.src.manager.project_manager import ProjectManager
from backend.src.manager.project_user_manager import ProjectUserManager
from backend.src.manager.project_staff_cost_manager import ProjectStaffCostManager



class ProjectManagerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create()
        self.group_id = 1 
        self.creator_user_id = self.user.id
        self.project_number = ProjectNumber.objects.create(project_number='P1')
        self.project_group = ProjectGroup.objects.create()
        self.project_status = ProjectStatus.objects.create(name='In Progress')
        self.project_type = ProjectType.objects.create(name='Type1')
        self.currency = Currency.objects.create(symbol='$', name='USD')
        self.file_group = FileGroup.objects.create(name='File1')
        self.customer = Customer.objects.create(company_name='company_name1')
        self.probability_of_nomination = 0.5 

        kwargs = {
            'name': 'Testproject1',
            'project_number': self.project_number,
            'project_group': self.project_group,
            'project_status': self.project_status,
            'project_type': self.project_type,
            'currency': self.currency,
            'file_group': self.file_group,
            'customer': self.customer,
            'probability_of_nomination': self.probability_of_nomination,
        }
        self.project_manager = ProjectManager.create(self.creator_user_id, **kwargs)

    def test_create(self): 
        kwargs = {
            'name': 'Testproject2',
            'project_number': self.project_number,
            'project_status': self.project_status,
            'project_type': self.project_type,
            'currency': self.currency,
            'file_group': self.file_group,
            'customer': self.customer,
            'probability_of_nomination': 0.7,
        }
        project_manager_obj = ProjectManager.create(self.creator_user_id, **kwargs)

        self.assertIsInstance(project_manager_obj, ProjectManager)
        
        obj = Project.objects.get(id=project_manager_obj.id)
        self.assertEqual(obj.name,'Testproject2')
        self.assertEqual(obj.project_number.project_number, 'P1')
        self.assertEqual(obj.project_group.id, 3)  
        self.assertEqual(obj.project_status.name,'In Progress')
        self.assertEqual(obj.project_type.name, 'Type1')
        self.assertEqual(obj.currency.name,'USD')
        self.assertEqual(obj.customer.company_name, 'company_name1')
        self.assertEqual(obj.probability_of_nomination,0.7)
 
    def test_filter(self):
        result = ProjectManager.filter(project_number = self.project_number, project_status = self.project_status)
        expected_result = [
            ProjectManager(project_group_id=self.project_manager.project_group) 
        ]
        self.assertEqual(result, expected_result)

    def test_update(self): 
        name_updated = 'TestProject1Updated'
        project_manager = ProjectManager(self.project_manager.project_group)
        project_manager.update(self.creator_user_id, name = name_updated) 

        updated_obj = Project.objects.latest('id')
        self.assertEqual(updated_obj.name, 'TestProject1Updated')


    def test_deactivate(self):
        project_manager = ProjectManager(self.project_manager.project_group) 
        obj = Project.objects.get(id=project_manager.id)
        self.assertTrue(obj.active)
        project_manager.deactivate(self.creator_user_id)
        deactivated_obj = Project.objects.latest('id')
        self.assertFalse(deactivated_obj.active)
   

class ProjectUserManagerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create()
        self.group_id = 1 
        self.creator_user_id = self.user.id

        self.project_group = ProjectGroup.objects.create()
        self.project_user_group = ProjectUserGroup.objects.create(user= self.user, project_group = self.project_group)
        self.project_user_role1 = ProjectUserRole.objects.create(name = 'role1')
        self.project_user_role2 = ProjectUserRole.objects.create(name = 'role2')   

        kwargs = {
            'user': self.user,
            'project_group': self.project_group,
            'project_user_group': self.project_user_group,
            'project_user_role_id_list' : [self.project_user_role1.id, self.project_user_role2.id]
        }
        self.project_user_manager_obj = ProjectUserManager.create(self.creator_user_id, **kwargs)
     
    def test_create(self): 
        kwargs = {
            'user': self.user,
            'project_group': self.project_group,
            'project_user_group': self.project_user_group,
            'project_user_role_id_list' : [self.project_user_role1.id, self.project_user_role2.id]
        }
        project_user_manager_obj = ProjectUserManager.create(self.creator_user_id, **kwargs)
        self.assertIsInstance(project_user_manager_obj, ProjectUserManager)
        obj = ProjectUser.objects.get(id=project_user_manager_obj.id)
        self.assertEqual(obj.project_user_role.count(), 2)
        self.assertTrue(obj.project_user_role.filter(name='role1').exists())
        self.assertTrue(obj.project_user_role.filter(name='role2').exists())


    def test_update(self): 
        project_user_role3 = ProjectUserRole.objects.create(name='role2')
        update = {
            'project_user_role_id_list': [self.project_user_role1.id, self.project_user_role2.id,project_user_role3.id]
        }
        project_user_manager = ProjectUserManager(self.project_user_manager_obj.project_user_group)
        project_user_manager.update(self.creator_user_id, **update)

        updated_obj = ProjectUser.objects.latest('id')
        self.assertEqual(updated_obj.project_user_role.count(), 3)
     

    def test_deactivate(self):
        project_user_manager = ProjectUserManager(self.project_user_manager_obj.project_user_group)
        obj = ProjectUser.objects.get(id = self.project_user_manager_obj.id)

        self.assertTrue(obj.active)
        project_user_manager.deactivate(self.creator_user_id)
        deactivated_obj = ProjectUser.objects.latest('id')
        self.assertFalse(deactivated_obj.active)

    def test_filter(self):
        filter_kwargs = {
            'project_user_role': self.project_user_role1,
        }
        result = ProjectUserManager.filter(**filter_kwargs)
        expected_result = [
            ProjectUserManager(project_user_group_id=self.project_user_manager_obj.project_user_group) 
        ]
        self.assertEqual(result, expected_result)    


class ProjectStaffCostManagerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create()
        self.group_id = 1 
        self.creator_user_id = self.user.id

        self.project_group = ProjectGroup.objects.create()
        self.project_staff_cost_task = ProjectStaffCostTask.objects.create()
        self.project_staff_cost_group = ProjectStaffCostGroup.objects.create(
            project_group = self.project_group,
            user = self.user,
            project_staff_cost_task = self.project_staff_cost_task,
            work_date = datetime.datetime.today()
        )  
        kwargs = {
            'project_staff_cost_group': self.project_staff_cost_group,
            'hours': 7.5,
            'work_date': datetime.date.today(),
            'project_staff_cost_task' : self.project_staff_cost_task,
            'user': self.user,
            'project_group': self.project_group
        }
        self.project_staff_cost_manager_obj = ProjectStaffCostManager.create(self.creator_user_id, **kwargs)

    def test_create(self): 
        kwargs = {
            'project_staff_cost_group': self.project_staff_cost_group,
            'hours': 7.5,
            'work_date': datetime.date.today(),
            'project_staff_cost_task' : self.project_staff_cost_task,
            'user': self.user,
            'project_group': self.project_group
        }
        project_staff_cost_manager_obj = ProjectStaffCostManager.create(self.creator_user_id, **kwargs)
        self.assertIsInstance(project_staff_cost_manager_obj, ProjectStaffCostManager)
        obj = ProjectStaffCost.objects.get(id=project_staff_cost_manager_obj.id)
        self.assertEqual(obj.hours, 7.5)
        self.assertTrue(obj.project_staff_cost_group.id, self.project_staff_cost_group.id)


    def test_update(self): 
        update = {
            'hours': 8.0
        }
        project_staff_cost_manager = ProjectStaffCostManager(self.project_staff_cost_manager_obj.project_staff_cost_group)
        project_staff_cost_manager.update(self.creator_user_id, **update)

        updated_obj = ProjectStaffCost.objects.latest('id')
        self.assertEqual(updated_obj.hours, 8.0)
     

    def test_deactivate(self):
        project_staff_cost_manager = ProjectStaffCostManager(self.project_staff_cost_manager_obj.project_staff_cost_group)
        obj = ProjectStaffCost.objects.get(id = self.project_staff_cost_manager_obj.id)

        self.assertTrue(obj.active)
        project_staff_cost_manager.deactivate(self.creator_user_id)
        deactivated_obj = ProjectStaffCost.objects.latest('id')
        self.assertFalse(deactivated_obj.active)

    def test_filter(self):
        filter_kwargs = {
            'hours': 7.5,
            'user' : self.user
        }
        result = ProjectStaffCostManager.filter(**filter_kwargs)
        expected_result = [
            ProjectStaffCostManager(project_staff_cost_group_id=self.project_staff_cost_manager_obj.project_staff_cost_group) 
        ]
        self.assertEqual(result, expected_result)    