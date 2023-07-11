import datetime
from django.test import TestCase
from backend.models import PatentClaim, Patent, PatentGroup, PatentClaimGroup, User, PatentTag, PatentTagGroup
from backend.src.manager.patent_tag_manager import PatentTagManager
from backend.src.manager.patent_manager import PatentManager
from backend.src.manager.patent_claim_manager import PatentClaimManager


class PatentTagManagerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create()
        self.group_id = 1 
        self.creator_user_id = self.user.id
        self.patent_tag_group = PatentTagGroup.objects.create()

        kwargs = {
            'text': 'A',
            'alt_text1' : 'B',
            'alt_text2' : 'C',
            'alt_text3' : 'D',
            'alt_text4' : 'E',
            'alt_text5' : 'F',
            'priority_date' : datetime.date.today(),
            'patent_tag_group': self.patent_tag_group
        }
        self.patent_tag_manager = PatentTagManager.create(self.creator_user_id, **kwargs)
       
    def test_create(self): 
        kwargs = {
            'text': 'A',
            'alt_text1' : 'B',
            'alt_text2' : 'C',
            'alt_text3' : 'D',
            'alt_text4' : 'E',
            'alt_text5' : 'F',
            'priority_date' : datetime.date.today(),
            'patent_tag_group': self.patent_tag_group
        }
        patent_tag_manager_obj = PatentTagManager.create(self.creator_user_id, **kwargs)

        self.assertIsInstance(patent_tag_manager_obj, PatentTagManager)
        
        obj = PatentTag.objects.get(id=patent_tag_manager_obj.id)
        self.assertEqual(obj.text, 'A' )  
        self.assertEqual(obj.alt_text1, 'B')
        self.assertEqual(obj.alt_text2, 'C')
        self.assertEqual(obj.alt_text3, 'D')
        self.assertEqual(obj.alt_text4, 'E')
        self.assertEqual(obj.alt_text5, 'F')
        self.assertEqual(obj.priority_date, patent_tag_manager_obj.priority_date)
        self.assertEqual(obj.patent_tag_group.id, 3)

    def test_update(self): 
        update = {
            'alt_text1': 'BNew',   
            'alt_text2': 'CNew'
        }
        patent_tag_manager = PatentTagManager(self.patent_tag_manager.patent_tag_group)
        patent_tag_manager.update(self.creator_user_id, **update)

        updated_obj = PatentTag.objects.latest('id')
        self.assertEqual(updated_obj.alt_text1, 'BNew')
        self.assertEqual(updated_obj.alt_text2, 'CNew')

    def test_deactivate(self):
        patent_tag_manager = PatentTagManager(self.patent_tag_manager.patent_tag_group)
        obj = PatentTag.objects.get(id=patent_tag_manager.id)

        self.assertTrue(obj.active)
        patent_tag_manager.deactivate(self.creator_user_id)
        deactivated_obj = PatentTag.objects.latest('id')
        self.assertFalse(deactivated_obj.active)
   
    def test_filter(self):
        filter_kwargs = {
            'text': 'A',
            'alt_text2': 'C'
        }
        result = PatentTagManager.filter(**filter_kwargs)
        expected_result = [
            PatentTagManager(patent_tag_group_id=self.patent_tag_manager.patent_tag_group) 
        ]
        self.assertEqual(result, expected_result)


class PatentManagerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create()
        self.group_id = 1 
        self.creator_user_id = self.user.id
        self.patent_group = PatentGroup.objects.create(patent_number = '123')

        kwargs = {
            'patent_group': self.patent_group,
            'remark' : 'remark',
            'abstract' : 'abstract',
            'priority_date' : datetime.date.today(),
            'patent_number': self.patent_group.patent_number 
        }
        self.patent_manager_obj = PatentManager.create(self.creator_user_id, **kwargs)

    def test_create(self):
        kwargs = {
            'patent_group': self.patent_group,
            'remark' : 'remark',
            'abstract' : 'abstract',
            'priority_date' : datetime.date.today(),
            'patent_number': self.patent_group.patent_number 
        }
        patent_manager_obj = PatentManager.create(self.creator_user_id, **kwargs)

        self.assertIsInstance(patent_manager_obj, PatentManager)
        
        obj = Patent.objects.get(id=patent_manager_obj.id)
        self.assertEqual(obj.remark, 'remark' )  
        self.assertEqual(obj.abstract, 'abstract')
        self.assertEqual(obj.priority_date, patent_manager_obj.priority_date)
        self.assertEqual(obj.patent_group.id, 3)

    def test_update(self): 
        update = {
            'remark': 'remarkNew',   
            'abstract': 'abstractNew',   

        }
        patent_manager = PatentManager(self.patent_manager_obj.patent_group)
        patent_manager.update(self.creator_user_id, **update)

        updated_obj = Patent.objects.latest('id')
        self.assertEqual(updated_obj.remark, 'remarkNew')
        self.assertEqual(updated_obj.abstract, 'abstractNew')

    def test_deactivate(self):
        patent_manager = PatentManager(2)
        obj = Patent.objects.get(id= self.patent_manager_obj.id)

        self.assertTrue(obj.active)
        patent_manager.deactivate(self.creator_user_id)
        deactivated_obj = Patent.objects.latest('id')
        self.assertFalse(deactivated_obj.active)
   
    def test_filter(self):
        filter_kwargs = {
            'abstract': 'abstract',
        }
        result = PatentManager.filter(**filter_kwargs)
        expected_result = [
            PatentManager(patent_group_id=self.patent_manager_obj.patent_group) 
        ]
        self.assertEqual(result, expected_result)    


class PatentClaimManagerTest(TestCase):
    
    def setUp(self):
        self.user = User.objects.create()
        self.group_id = 1 
        self.creator_user_id = self.user.id
        self.patent_group = PatentGroup.objects.create()
        self.patent_claim_group = PatentClaimGroup.objects.create(patent_group = self.patent_group)

        kwargs = {
            'patent_claim_group': self.patent_group,
            'text' : 'text',
            'patent_group': self.patent_group
        }
        self.patent_claim_manager = PatentClaimManager.create(self.creator_user_id, **kwargs)

    def test_create(self):
        kwargs = {
            'patent_claim_group': self.patent_group,
            'text' : 'text',
            'patent_group': self.patent_group
        }
        patent_claim_manager= PatentClaimManager.create(self.creator_user_id, **kwargs)

        self.assertIsInstance(patent_claim_manager, PatentClaimManager)
        
        obj = PatentClaim.objects.get(id=patent_claim_manager.id)
        self.assertEqual(obj.text, 'text')  
        self.assertEqual(obj.patent_claim_group.id, 3) #setUp data kwargs group_id 2 already

    def test_update(self): 
        update = {
            'text': 'textNew',   
        }
        patent_claim_manager = PatentClaimManager(self.patent_claim_manager.patent_claim_group)
        patent_claim_manager.update(self.creator_user_id, **update)

        updated_obj = PatentClaim.objects.latest('id')
        self.assertEqual(updated_obj.text, 'textNew')

    def test_deactivate(self):
        patent_claim_manager = PatentClaimManager(self.patent_claim_manager.patent_claim_group)
        obj = PatentClaim.objects.get(id= self.patent_claim_manager.id)

        self.assertTrue(obj.active)
        patent_claim_manager.deactivate(self.creator_user_id)
        deactivated_obj = PatentClaim.objects.latest('id')
        self.assertFalse(deactivated_obj.active)
   
    def test_filter(self):
        filter_kwargs = {
            'text': 'text',
        }
        result = PatentClaimManager.filter(**filter_kwargs)
        expected_result = [
            PatentClaimManager(patent_claim_group_id= self.patent_claim_manager.patent_claim_group) 
        ]
        self.assertEqual(result, expected_result)    

