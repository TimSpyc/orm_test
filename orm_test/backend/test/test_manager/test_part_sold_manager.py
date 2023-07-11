import datetime
from django.test import TestCase
from backend.models import Source, PartGroup, PartRecipient, PartSoldCustomerPrice, PartSoldCustomerPriceGroup, PartSoldMaterialPrice, PartSoldMaterialPriceGroup, PartSoldMaterialPriceType, PartSoldMaterialType, PartSoldMaterialWeight, PartSoldMaterialWeightGroup, PartSoldPrice, PartSoldPriceGroup, PartSoldPriceSaving, PartSoldPriceSavingGroup, PartSoldPriceType, PartSoldUploadedPrice, PartSoldUploadedPriceGroup, SavingUnit, User, PartSoldGroup, SapNumber, Customer, CustomerPlant, ContractGroup, Currency, PartSold
from backend.src.manager.part_sold_customer_price_manager import PartSoldCustomerPriceManager
from backend.src.manager.part_sold_manager import PartSoldManager
from backend.src.manager.part_sold_material_price_manager import PartSoldMaterialPriceManager
from backend.src.manager.part_sold_material_weight_manager import PartSoldMaterialWeightManager
from backend.src.manager.part_sold_price_manager import PartSoldPriceManager
from backend.src.manager.part_sold_price_saving_manager import PartSoldPriceSavingManager
from backend.src.manager.part_sold_uploaded_price_manager import PartSoldUploadedPriceManager



class PartSoldManagerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create()
        self.group_id = 1 
        self.creator_user_id = self.user.id
        self.part_group = PartGroup.objects.create()
        self.part_recipient = PartRecipient.objects.create()
        self.part_sold_group = PartSoldGroup.objects.create(
            part_recipient = self.part_recipient,
            customer_part_number_sap = '12345'
        )
        self.sap_number = SapNumber.objects.create()
        self.customer = Customer.objects.create()
        self.customer_plant = CustomerPlant.objects.create(
            customer = self.customer
        )
        self.contract_group = ContractGroup.objects.create(
            contract_number = '123abc',
            contract_date = datetime.date.today()
        )
        self.currency = Currency.objects.create()

        kwargs = {
                'sap_number': self.sap_number,
                'part_sold_group': self.part_sold_group,
                'customer_part_number': 'ABCDE',
                'part_group_id_list' : [self.part_group.id],
                'customer_plant': self.customer_plant,
                'contract_group': self.contract_group,
                'customer_plant': self.customer_plant,
                'currency': self.currency,
                'description': 'Description',
                'validity_start_date': datetime.date.today(),
                'validity_end_date': datetime.date.today(),
                'cbd_date': datetime.date.today(),
                'part_recipient': self.part_recipient,
                'customer_part_number_sap': self.part_sold_group.customer_part_number_sap
           }
        self.part_sold_manager_obj = PartSoldManager.create(self.creator_user_id, **kwargs)

    
    def test_create(self):
        kwargs = {
                'sap_number': self.sap_number,
                'part_sold_group': self.part_sold_group,
                'customer_part_number': 'ABCDE',
                'part_group_id_list' : [self.part_group.id],
                'customer_plant': self.customer_plant,
                'contract_group': self.contract_group,
                'customer_plant': self.customer_plant,
                'currency': self.currency,
                'description': 'Description',
                'validity_start_date':datetime.date(2023,1,1),
                'validity_end_date':datetime.date(2023,2,2),
                'cbd_date':datetime.date(2023,3,3),
                'part_recipient': self.part_recipient,
                'customer_part_number_sap': self.part_sold_group.customer_part_number_sap
           }
        part_sold_manager_obj = PartSoldManager.create(self.creator_user_id, **kwargs)
        self.assertIsInstance(part_sold_manager_obj, PartSoldManager)
        
        obj = PartSold.objects.get(id=part_sold_manager_obj.id) 

        self.assertEqual(obj.customer_part_number, 'ABCDE')
        self.assertEqual(obj.description, 'Description')
        self.assertEqual(obj.currency, self.currency)
        self.assertEqual(obj.sap_number.id, self.sap_number.id)
        self.assertEqual(obj.part_sold_group.id, self.part_sold_group.id)
        self.assertEqual(obj.customer_plant.id, self.customer_plant.id)
        self.assertEqual(obj.contract_group.id, self.contract_group.id)
        self.assertEqual(obj.validity_start_date, part_sold_manager_obj.validity_start_date)
        self.assertEqual(obj.validity_start_date, part_sold_manager_obj.validity_start_date)
        self.assertEqual(obj.validity_end_date, part_sold_manager_obj.validity_end_date)
        self.assertEqual(obj.cbd_date, part_sold_manager_obj.cbd_date)
        self.assertTrue(obj.part_group.filter(id=self.part_group.id).exists())

    def test_update(self): 
        update = {
            'customer_part_number' : 'EDCBA' 
        }
        part_sold_manager = PartSoldManager(self.part_sold_manager_obj.part_sold_group)
        part_sold_manager.update(self.creator_user_id, **update)

        updated_obj = PartSold.objects.latest('id')
        self.assertEqual(updated_obj.customer_part_number, 'EDCBA' )
        self.assertEqual(updated_obj.part_sold_group.id, self.part_sold_group.id)

    def test_deactivate(self):
        part_sold_manager = PartSoldManager(self.part_sold_manager_obj.part_sold_group)
        obj = PartSold.objects.get(id = self.part_sold_manager_obj.id)

        self.assertTrue(obj.active)
        part_sold_manager.deactivate(self.creator_user_id)
        deactivated_obj = PartSold.objects.latest('id')
        self.assertFalse(deactivated_obj.active)

    def test_filter(self):
        filter_kwargs = {
                'description': 'Description',
                'customer_plant': self.customer_plant
        }
        result = PartSoldManager.filter(**filter_kwargs)
        expected_result = [
            PartSoldManager(part_sold_group_id=self.part_sold_manager_obj.part_sold_group) 
        ]
        self.assertEqual(result, expected_result) 


class PartSoldPriceManagerTest(TestCase):

    def setUp(self):
        self.user = User.objects.create()
        self.group_id = 1 
        self.creator_user_id = self.user.id
        self.part_sold_price_type = PartSoldPriceType.objects.create()
        self.part_group = PartGroup.objects.create()
        self.part_recipient = PartRecipient.objects.create()
        self.part_sold_group = PartSoldGroup.objects.create(
            part_recipient = self.part_recipient,
            customer_part_number_sap = '12345'
        )
        self.sap_number = SapNumber.objects.create()
        self.customer = Customer.objects.create()
        self.customer_plant = CustomerPlant.objects.create(
            customer = self.customer
        )
        self.contract_group = ContractGroup.objects.create(
            contract_number = '123abc',
            contract_date = datetime.date.today()
        )
        self.currency = Currency.objects.create()

        kwargs = {
                'sap_number': self.sap_number,
                'part_sold_group': self.part_sold_group,
                'customer_part_number': 'ABCDE',
                'part_group_id_list' : [self.part_group.id],
                'customer_plant': self.customer_plant,
                'contract_group': self.contract_group,
                'customer_plant': self.customer_plant,
                'currency': self.currency,
                'description': 'Description',
                'validity_start_date':datetime.date(2023,1,1),
                'validity_end_date':datetime.date(2023,2,2),
                'cbd_date':datetime.date(2023,3,3),
                'part_recipient': self.part_recipient,
                'customer_part_number_sap': self.part_sold_group.customer_part_number_sap
           }
        part_sold_manager_obj = PartSoldManager.create(self.creator_user_id, **kwargs)
        self.part_sold = PartSold.objects.get(id=part_sold_manager_obj.id) 


        self.part_sold_price_group = PartSoldPriceGroup.objects.create(
            part_sold = self.part_sold,
            part_sold_price_type = self.part_sold_price_type
        )

        kwargs = {
                'part_sold_price_group': self.part_sold_price_group,
                'value': 123,
                'saveable': 12000,
                'part_sold_price_type': self.part_sold_price_type,
                'part_sold' : self.part_sold_price_group.part_sold
           }
        self.part_sold_price_manager_obj = PartSoldPriceManager.create(self.creator_user_id, **kwargs)
    
    def test_create(self):
        kwargs = {
                'part_sold_price_group': self.part_sold_price_group,
                'value': 123,
                'saveable': 12000,
                'part_sold_price_type': self.part_sold_price_type,
                'part_sold' : self.part_sold_price_group.part_sold
           }
        part_sold_price_manager_obj = PartSoldPriceManager.create(self.creator_user_id, **kwargs)
        self.assertIsInstance(part_sold_price_manager_obj, PartSoldPriceManager)

        obj = PartSoldPrice.objects.get(id=part_sold_price_manager_obj.id) 
        self.assertEqual(obj.part_sold_price_group.id, self.part_sold_price_group.id)
        self.assertEqual(obj.value, 123)
        self.assertEqual(obj.saveable, 12000)
        self.assertEqual(obj.part_sold_price_group.part_sold_price_type, self.part_sold_price_type)
        self.assertEqual(obj.part_sold_price_group.part_sold, self.part_sold)


    def test_update(self): 
        update = {
            'value' : 123
        }
        part_sold_price_manager = PartSoldPriceManager(self.part_sold_price_manager_obj.part_sold_price_group)
        part_sold_price_manager.update(self.creator_user_id, **update)

        updated_obj = PartSoldPrice.objects.latest('id')
        self.assertEqual(updated_obj.value, 123)

    def test_deactivate(self):
        part_sold_price_manager = PartSoldPriceManager(self.part_sold_price_manager_obj.part_sold_price_group)
        obj = PartSoldPrice.objects.get(id = self.part_sold_price_manager_obj.id)

        self.assertTrue(obj.active)
        part_sold_price_manager.deactivate(self.creator_user_id)
        deactivated_obj = PartSoldPrice.objects.latest('id')
        self.assertFalse(deactivated_obj.active)

    def test_filter(self):
        filter_kwargs = {
                'value' : 123,
        }
        result = PartSoldPriceManager.filter(**filter_kwargs)
        expected_result = [
            PartSoldPriceManager(part_sold_price_group_id=self.part_sold_price_manager_obj.part_sold_price_group) 
        ]
        self.assertEqual(result, expected_result) 


class PartSoldCustomerPriceManagerTest(TestCase):

    def setUp(self):
        self.user = User.objects.create()
        self.group_id = 1 
        self.creator_user_id = self.user.id
        self.part_sold_price_type = PartSoldPriceType.objects.create()
        self.part_group = PartGroup.objects.create()
        self.part_recipient = PartRecipient.objects.create()
        self.part_sold_group = PartSoldGroup.objects.create(
            part_recipient = self.part_recipient,
            customer_part_number_sap = '12345'
        )
        self.sap_number = SapNumber.objects.create()
        self.customer = Customer.objects.create()
        self.customer_plant = CustomerPlant.objects.create(
            customer = self.customer
        )
        self.contract_group = ContractGroup.objects.create(
            contract_number = '123abc',
            contract_date = datetime.date.today()
        )
        self.currency = Currency.objects.create()

        kwargs = {
                'sap_number': self.sap_number,
                'part_sold_group': self.part_sold_group,
                'customer_part_number': 'ABCDE',
                'part_group_id_list' : [self.part_group.id],
                'customer_plant': self.customer_plant,
                'contract_group': self.contract_group,
                'customer_plant': self.customer_plant,
                'currency': self.currency,
                'description': 'Description',
                'validity_start_date':datetime.date(2023,1,1),
                'validity_end_date':datetime.date(2023,2,2),
                'cbd_date':datetime.date(2023,3,3),
                'part_recipient': self.part_recipient,
                'customer_part_number_sap': self.part_sold_group.customer_part_number_sap
           }
        part_sold_manager_obj = PartSoldManager.create(self.creator_user_id, **kwargs)
        self.part_sold = PartSold.objects.get(id=part_sold_manager_obj.id) 

        self.part_sold_price_group = PartSoldPriceGroup.objects.create(
            part_sold = self.part_sold,
            part_sold_price_type = self.part_sold_price_type
        )
        self.part_sold_customer_price_group = PartSoldCustomerPriceGroup.objects.create(
            part_sold = self.part_sold,
            part_sold_price_type = self.part_sold_price_type,
            price_date = datetime.date.today()
        )

        kwargs = {
                'part_sold_customer_price_group': self.part_sold_customer_price_group,
                'value': 1234,
                'part_sold_price_type': self.part_sold_price_type,
                'part_sold' : self.part_sold,
                'price_date': datetime.date.today()
           }
        self.part_sold_customer_price_manager_obj = PartSoldCustomerPriceManager.create(self.creator_user_id, **kwargs)

    
    def test_create(self):
        kwargs = {
                'part_sold_customer_price_group': self.part_sold_customer_price_group,
                'value': 1234,
                'part_sold_price_type': self.part_sold_price_type,
                'part_sold' : self.part_sold,
                'price_date': datetime.date.today()
           }
        part_sold_customer_price_manager_obj = PartSoldCustomerPriceManager.create(self.creator_user_id, **kwargs)
        self.assertIsInstance(part_sold_customer_price_manager_obj, PartSoldCustomerPriceManager)
        obj = PartSoldCustomerPrice.objects.get(id=part_sold_customer_price_manager_obj.id) 
        self.assertEqual(obj.part_sold_customer_price_group.id, self.part_sold_customer_price_group.id)
        self.assertEqual(obj.value, 1234)

    def test_update(self): 
        update = {
            'value' : 12345
        }
        part_sold_customer_price_manager = PartSoldCustomerPriceManager(self.part_sold_customer_price_manager_obj.part_sold_customer_price_group)
        part_sold_customer_price_manager.update(self.creator_user_id, **update)
        updated_obj = PartSoldCustomerPrice.objects.latest('id')
        self.assertEqual(updated_obj.value, 12345)

    def test_deactivate(self):
        part_sold_customer_price_manager = PartSoldCustomerPriceManager(self.part_sold_customer_price_manager_obj.part_sold_customer_price_group)
        obj = PartSoldCustomerPrice.objects.get(id = self.part_sold_customer_price_manager_obj.id)

        self.assertTrue(obj.active)
        part_sold_customer_price_manager.deactivate(self.creator_user_id)
        deactivated_obj = PartSoldCustomerPrice.objects.latest('id')
        self.assertFalse(deactivated_obj.active)

    def test_filter(self):
        filter_kwargs = {
                'value' : 1234,
        }
        result = PartSoldCustomerPriceManager.filter(**filter_kwargs)
        expected_result = [
            PartSoldCustomerPriceManager(part_sold_customer_price_group_id=self.part_sold_customer_price_manager_obj.part_sold_customer_price_group) 
        ]
        self.assertEqual(result, expected_result)


class PartSoldUploadedPriceManagerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create()
        self.group_id = 1 
        self.creator_user_id = self.user.id
        self.part_sold_price_type = PartSoldPriceType.objects.create()
        self.part_group = PartGroup.objects.create()
        self.part_recipient = PartRecipient.objects.create()
        self.part_sold_group = PartSoldGroup.objects.create(
            part_recipient = self.part_recipient,
            customer_part_number_sap = '12345'
        )
        self.sap_number = SapNumber.objects.create()
        self.customer = Customer.objects.create()
        self.customer_plant = CustomerPlant.objects.create(
            customer = self.customer
        )
        self.contract_group = ContractGroup.objects.create(
            contract_number = '123abc',
            contract_date = datetime.date.today()
        )
        self.currency = Currency.objects.create()

        kwargs = {
                'sap_number': self.sap_number,
                'part_sold_group': self.part_sold_group,
                'customer_part_number': 'ABCDE',
                'part_group_id_list' : [self.part_group.id],
                'customer_plant': self.customer_plant,
                'contract_group': self.contract_group,
                'customer_plant': self.customer_plant,
                'currency': self.currency,
                'description': 'Description',
                'validity_start_date':datetime.date(2023,1,1),
                'validity_end_date':datetime.date(2023,2,2),
                'cbd_date':datetime.date(2023,3,3),
                'part_recipient': self.part_recipient,
                'customer_part_number_sap': self.part_sold_group.customer_part_number_sap
           }
        part_sold_manager_obj = PartSoldManager.create(self.creator_user_id, **kwargs)
        self.part_sold = PartSold.objects.get(id=part_sold_manager_obj.id) 

        self.part_sold_uploaded_price_group = PartSoldUploadedPriceGroup.objects.create(
            part_sold = self.part_sold,
            validity_start_date = datetime.date.today()
        )
        self.source = Source.objects.create()
        kwargs = {
                'part_sold_uploaded_price_group': self.part_sold_uploaded_price_group,
                'value': 1234567,
                'lme_basis': 0.1,
                'ecdp_basis': 0.2,
                'billet_basis': 0.3,
                'source': self.source,
                'description': 'Description',
                'part_sold': self.part_sold,
                'validity_start_date' : datetime.date.today()
           }
        self.part_sold_uploaded_price_manager_obj = PartSoldUploadedPriceManager.create(self.creator_user_id, **kwargs)

    def test_create(self):
        kwargs = {
                'part_sold_uploaded_price_group': self.part_sold_uploaded_price_group,
                'value': 1234567,
                'lme_basis': 0.1,
                'ecdp_basis': 0.2,
                'billet_basis': 0.3,
                'source': self.source,
                'description': 'Description',
                'part_sold': self.part_sold,
                'validity_start_date' : datetime.date.today()
           }
        part_sold_uploaded_price_manager_obj = PartSoldUploadedPriceManager.create(self.creator_user_id, **kwargs)

        self.assertIsInstance(part_sold_uploaded_price_manager_obj, PartSoldUploadedPriceManager)
        obj = PartSoldUploadedPrice.objects.get(id=part_sold_uploaded_price_manager_obj.id) 
        self.assertEqual(obj.part_sold_uploaded_price_group.id, self.part_sold_uploaded_price_group.id)
        self.assertEqual(obj.value, 1234567)
        self.assertEqual(obj.lme_basis, 0.1)
        self.assertEqual(obj.ecdp_basis, 0.2)
        self.assertEqual(obj.billet_basis, 0.3)
        self.assertEqual(obj.source, self.source)
        self.assertEqual(obj.description, 'Description')


    def test_update(self): 
        update = {
            'value' : 12345678,
            'billet_basis' : 0.4
        }
        part_sold_uploaded_price_manager = PartSoldUploadedPriceManager(self.part_sold_uploaded_price_manager_obj.part_sold_uploaded_price_group)
        part_sold_uploaded_price_manager.update(self.creator_user_id, **update)

        updated_obj = PartSoldUploadedPrice.objects.latest('id')
        self.assertEqual(updated_obj.value, 12345678)

    def test_deactivate(self):
        part_sold_uploaded_price_manager = PartSoldUploadedPriceManager(self.part_sold_uploaded_price_manager_obj.part_sold_uploaded_price_group)
        obj = PartSoldUploadedPrice.objects.get(id = self.part_sold_uploaded_price_manager_obj.id)

        self.assertTrue(obj.active)
        part_sold_uploaded_price_manager.deactivate(self.creator_user_id)
        deactivated_obj = PartSoldUploadedPrice.objects.latest('id')
        self.assertFalse(deactivated_obj.active)

    def test_filter(self):
        filter_kwargs = {
                'value' : 1234567,
                'source': self.source
        }
        result = PartSoldUploadedPriceManager.filter(**filter_kwargs)
        expected_result = [
            PartSoldUploadedPriceManager(part_sold_uploaded_price_group_id=self.part_sold_uploaded_price_manager_obj.part_sold_uploaded_price_group) 
        ]
        self.assertEqual(result, expected_result)


class PartSoldMaterialPriceManagerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create()
        self.group_id = 1 
        self.creator_user_id = self.user.id
        self.part_sold_price_type = PartSoldPriceType.objects.create()
        self.part_group = PartGroup.objects.create()
        self.part_recipient = PartRecipient.objects.create()
        self.part_sold_group = PartSoldGroup.objects.create(
            part_recipient = self.part_recipient,
            customer_part_number_sap = '12345'
        )
        self.sap_number = SapNumber.objects.create()
        self.customer = Customer.objects.create()
        self.customer_plant = CustomerPlant.objects.create(
            customer = self.customer
        )
        self.contract_group = ContractGroup.objects.create(
            contract_number = '123abc',
            contract_date = datetime.date.today()
        )
        self.currency = Currency.objects.create()

        kwargs = {
                'sap_number': self.sap_number,
                'part_sold_group': self.part_sold_group,
                'customer_part_number': 'ABCDE',
                'part_group_id_list' : [self.part_group.id],
                'customer_plant': self.customer_plant,
                'contract_group': self.contract_group,
                'customer_plant': self.customer_plant,
                'currency': self.currency,
                'description': 'Description',
                'validity_start_date':datetime.date(2023,1,1),
                'validity_end_date':datetime.date(2023,2,2),
                'cbd_date':datetime.date(2023,3,3),
                'part_recipient': self.part_recipient,
                'customer_part_number_sap': self.part_sold_group.customer_part_number_sap
           }
        part_sold_manager_obj = PartSoldManager.create(self.creator_user_id, **kwargs)
        self.part_sold = PartSold.objects.get(id=part_sold_manager_obj.id) 

        self.part_sold_material_price_type = PartSoldMaterialPriceType.objects.create()    
        self.part_sold_material_price_group = PartSoldMaterialPriceGroup.objects.create(
            part_sold = self.part_sold,
            part_sold_material_price_type = self.part_sold_material_price_type
        )
        
        kwargs = {
                'part_sold_material_price_group': self.part_sold_material_price_group,
                'variable': True,
                'basis': 100.0,
                'use_gross_weight' : True,
                'saveable': True,
                'part_sold': self.part_sold,
                'part_sold_material_price_type' : self.part_sold_material_price_type
           }
        self.part_sold_material_price_manager_obj = PartSoldMaterialPriceManager.create(self.creator_user_id, **kwargs)

    def test_create(self):
        kwargs = {
                'part_sold_material_price_group': self.part_sold_material_price_group,
                'variable': True,
                'basis': 11.0,
                'use_gross_weight' : True,
                'saveable': True,
                'part_sold': self.part_sold,
                'part_sold_material_price_type' : self.part_sold_material_price_type
           }
        part_sold_material_price_manager_obj = PartSoldMaterialPriceManager.create(self.creator_user_id, **kwargs)

        self.assertIsInstance(part_sold_material_price_manager_obj, PartSoldMaterialPriceManager)
        obj = PartSoldMaterialPrice.objects.get(id=part_sold_material_price_manager_obj.id) 
        self.assertEqual(obj.part_sold_material_price_group.id, self.part_sold_material_price_group.id)
        self.assertTrue(obj.variable)
        self.assertEqual(obj.basis, 11.0)
        self.assertTrue(obj.saveable)
        self.assertTrue(obj.use_gross_weight)
        self.assertEqual(obj.part_sold_material_price_group.part_sold, self.part_sold)
        self.assertEqual(obj.part_sold_material_price_group.part_sold_material_price_type, self.part_sold_material_price_type)
       

    def test_update(self): 
        update = {
            'basis' : 11.0
        }
        part_sold_material_price_manager = PartSoldMaterialPriceManager(self.part_sold_material_price_manager_obj.part_sold_material_price_group)
        part_sold_material_price_manager.update(self.creator_user_id, **update)

        updated_obj = PartSoldMaterialPrice.objects.latest('id')
        self.assertEqual(updated_obj.part_sold_material_price_group.part_sold, self.part_sold)
        self.assertEqual(updated_obj.basis, 11.0)

    def test_deactivate(self):
        part_sold_material_price_manager = PartSoldMaterialPriceManager(self.part_sold_material_price_manager_obj.part_sold_material_price_group)
        obj = PartSoldMaterialPrice.objects.get(id = self.part_sold_material_price_manager_obj.id)

        self.assertTrue(obj.active)
        part_sold_material_price_manager.deactivate(self.creator_user_id)
        deactivated_obj = PartSoldMaterialPrice.objects.latest('id')
        self.assertFalse(deactivated_obj.active)

    def test_filter(self):
        filter_kwargs = {
                'part_sold' : self.part_sold,
                'variable': True
        }
        result = PartSoldMaterialPriceManager.filter(**filter_kwargs)
        expected_result = [
            PartSoldMaterialPriceManager(part_sold_material_price_group_id=self.part_sold_material_price_manager_obj.part_sold_material_price_group) 
        ]
        self.assertEqual(result, expected_result)


class PartSoldMaterialWeightManagerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create()
        self.group_id = 1 
        self.creator_user_id = self.user.id
        self.part_sold_price_type = PartSoldPriceType.objects.create()
        self.part_group = PartGroup.objects.create()
        self.part_recipient = PartRecipient.objects.create()
        self.part_sold_group = PartSoldGroup.objects.create(
            part_recipient = self.part_recipient,
            customer_part_number_sap = '12345'
        )
        self.sap_number = SapNumber.objects.create()
        self.customer = Customer.objects.create()
        self.customer_plant = CustomerPlant.objects.create(
            customer = self.customer
        )
        self.contract_group = ContractGroup.objects.create(
            contract_number = '123abc',
            contract_date = datetime.date.today()
        )
        self.currency = Currency.objects.create()

        kwargs = {
                'sap_number': self.sap_number,
                'part_sold_group': self.part_sold_group,
                'customer_part_number': 'ABCDE',
                'part_group_id_list' : [self.part_group.id],
                'customer_plant': self.customer_plant,
                'contract_group': self.contract_group,
                'customer_plant': self.customer_plant,
                'currency': self.currency,
                'description': 'Description',
                'validity_start_date':datetime.date(2023,1,1),
                'validity_end_date':datetime.date(2023,2,2),
                'cbd_date':datetime.date(2023,3,3),
                'part_recipient': self.part_recipient,
                'customer_part_number_sap': self.part_sold_group.customer_part_number_sap
           }
        part_sold_manager_obj = PartSoldManager.create(self.creator_user_id, **kwargs)
        self.part_sold = PartSold.objects.get(id=part_sold_manager_obj.id) 

        self.part_sold_material_type = PartSoldMaterialType.objects.create()    
        self.part_sold_material_weight_group = PartSoldMaterialWeightGroup.objects.create(
            part_sold = self.part_sold,
            part_sold_material_type = self.part_sold_material_type
        )
        
        kwargs = {
                'part_sold_material_weight_group': self.part_sold_material_weight_group,
                'gross_weight': 12.3,
                'net_weight': 45.6,
                'part_sold': self.part_sold,
                'part_sold_material_type' : self.part_sold_material_type
           }
        self.part_sold_material_weight_manager_obj = PartSoldMaterialWeightManager.create(self.creator_user_id, **kwargs)

    def test_create(self):
        kwargs = {
                'part_sold_material_weight_group': self.part_sold_material_weight_group,
                'gross_weight': 12.3,
                'net_weight': 45.6,
                'part_sold': self.part_sold,
                'part_sold_material_type' : self.part_sold_material_type
           }
        part_sold_material_weight_manager_obj = PartSoldMaterialWeightManager.create(self.creator_user_id, **kwargs)

        self.assertIsInstance(part_sold_material_weight_manager_obj, PartSoldMaterialWeightManager)
        obj = PartSoldMaterialWeight.objects.get(id=part_sold_material_weight_manager_obj.id) 
        self.assertEqual(obj.part_sold_material_weight_group.id, self.part_sold_material_weight_group.id)
        self.assertEqual(obj.net_weight, 45.6)
        self.assertEqual(obj.gross_weight, 12.3)
        self.assertEqual(obj.part_sold_material_weight_group.part_sold, self.part_sold)
        self.assertEqual(obj.part_sold_material_weight_group.part_sold_material_type, self.part_sold_material_type)
       

    def test_update(self): 
        update = {
            'gross_weight' : 1.0
        }
        part_sold_material_weight_manager = PartSoldMaterialWeightManager(self.part_sold_material_weight_manager_obj.part_sold_material_weight_group)
        part_sold_material_weight_manager.update(self.creator_user_id, **update)

        updated_obj = PartSoldMaterialWeight.objects.latest('id')
        self.assertEqual(updated_obj.part_sold_material_weight_group.part_sold, self.part_sold)
        self.assertEqual(updated_obj.gross_weight, 1.0)

    def test_deactivate(self):
        part_sold_material_weight_manager = PartSoldMaterialWeightManager(self.part_sold_material_weight_manager_obj.part_sold_material_weight_group)
        obj = PartSoldMaterialWeight.objects.get(id = self.part_sold_material_weight_manager_obj.id)

        self.assertTrue(obj.active)
        part_sold_material_weight_manager.deactivate(self.creator_user_id)
        deactivated_obj = PartSoldMaterialWeight.objects.latest('id')
        self.assertFalse(deactivated_obj.active)

    def test_filter(self):
        filter_kwargs = {
                'part_sold' : self.part_sold,
                'gross_weight': 12.3
        }
        result = PartSoldMaterialWeightManager.filter(**filter_kwargs)
        expected_result = [
            PartSoldMaterialWeightManager(part_sold_material_weight_group_id=self.part_sold_material_weight_manager_obj.part_sold_material_weight_group) 
        ]
        self.assertEqual(result, expected_result)    
    

class PartSoldPriceSavingManagerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create()
        self.group_id = 1 
        self.creator_user_id = self.user.id
        self.part_sold_price_type = PartSoldPriceType.objects.create()
        self.part_group = PartGroup.objects.create()
        self.part_recipient = PartRecipient.objects.create()
        self.part_sold_group = PartSoldGroup.objects.create(
            part_recipient = self.part_recipient,
            customer_part_number_sap = '12345'
        )
        self.sap_number = SapNumber.objects.create()
        self.customer = Customer.objects.create()
        self.customer_plant = CustomerPlant.objects.create(
            customer = self.customer
        )
        self.contract_group = ContractGroup.objects.create(
            contract_number = '123abc',
            contract_date = datetime.date.today()
        )
        self.currency = Currency.objects.create()

        kwargs = {
                'sap_number': self.sap_number,
                'part_sold_group': self.part_sold_group,
                'customer_part_number': 'ABCDE',
                'part_group_id_list' : [self.part_group.id],
                'customer_plant': self.customer_plant,
                'contract_group': self.contract_group,
                'customer_plant': self.customer_plant,
                'currency': self.currency,
                'description': 'Description',
                'validity_start_date':datetime.date(2023,1,1),
                'validity_end_date':datetime.date(2023,2,2),
                'cbd_date':datetime.date(2023,3,3),
                'part_recipient': self.part_recipient,
                'customer_part_number_sap': self.part_sold_group.customer_part_number_sap
           }
        part_sold_manager_obj = PartSoldManager.create(self.creator_user_id, **kwargs)
        self.part_sold = PartSold.objects.get(id=part_sold_manager_obj.id) 

        self.saving_unit = SavingUnit.objects.create()
        self.part_sold_price_saving_group = PartSoldPriceSavingGroup.objects.create(
            part_sold = self.part_sold,
            saving_date = datetime.date.today()
        )
        
        kwargs = {
                'part_sold_price_saving_group': self.part_sold_price_saving_group,
                'saving_rate': 12.3,
                'saving_unit': self.saving_unit,
                'part_sold': self.part_sold,
                'saving_date' : datetime.date(2023,3,3)
           }
        self.part_sold_price_saving_manager_obj = PartSoldPriceSavingManager.create(self.creator_user_id, **kwargs)
        self.saving_date = datetime.datetime(2023,3,3)
    def test_create(self):
        kwargs = {
                'part_sold_price_saving_group': self.part_sold_price_saving_group,
                'saving_rate': 12.3,
                'saving_unit': self.saving_unit,
                'part_sold': self.part_sold,
                'saving_date' : self.saving_date
           }
        part_sold_price_saving_manager_obj = PartSoldPriceSavingManager.create(self.creator_user_id, **kwargs)

        self.assertIsInstance(part_sold_price_saving_manager_obj, PartSoldPriceSavingManager)
        obj = PartSoldPriceSaving.objects.get(id=part_sold_price_saving_manager_obj.id) 
        self.assertEqual(obj.part_sold_price_saving_group.id, 2)
        self.assertEqual(obj.saving_rate, 12.3)
        self.assertEqual(obj.saving_unit, self.saving_unit)
        self.assertEqual(obj.part_sold_price_saving_group.part_sold, self.part_sold)
        self.assertEqual(obj.part_sold_price_saving_group.saving_date, self.saving_date)
       

    def test_update(self): 
        update = {
            'saving_rate': 15.7,
            'saving_unit': self.saving_unit,
        }
        part_sold_price_saving_manager = PartSoldPriceSavingManager(self.part_sold_price_saving_manager_obj.part_sold_price_saving_group)
        part_sold_price_saving_manager.update(self.creator_user_id, **update)

        updated_obj = PartSoldPriceSaving.objects.latest('id')
        self.assertEqual(updated_obj.part_sold_price_saving_group.part_sold, self.part_sold)
        self.assertEqual(updated_obj.saving_rate, 15.7)

    def test_deactivate(self):
        part_sold_price_saving_manager = PartSoldPriceSavingManager(self.part_sold_price_saving_manager_obj.part_sold_price_saving_group)
        obj = PartSoldPriceSaving.objects.get(id = self.part_sold_price_saving_manager_obj.id)

        self.assertTrue(obj.active)
        part_sold_price_saving_manager.deactivate(self.creator_user_id)
        deactivated_obj = PartSoldPriceSaving.objects.latest('id')
        self.assertFalse(deactivated_obj.active)

    def test_filter(self):
        filter_kwargs = {
            'saving_rate': 12.3,
            'saving_unit': self.saving_unit,
        }
        result = PartSoldPriceSavingManager.filter(**filter_kwargs)
        expected_result = [
            PartSoldPriceSavingManager(part_sold_price_saving_group_id=self.part_sold_price_saving_manager_obj.part_sold_price_saving_group) 
        ]
        self.assertEqual(result, expected_result)   