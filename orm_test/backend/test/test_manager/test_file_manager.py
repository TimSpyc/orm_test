from unittest import TestCase
from io import BytesIO
from PIL import Image
from backend.models import File, FileExtension, FileGroup, User, FileType
from backend.src.manager.file_manager import FileManager   

class FileManagerTest(TestCase):

    def setUp(self):
        User.objects.all().delete()
        self.user = User.objects.create(
            microsoft_id = '12345',
            first_name = 'Tim'
        )

        self.group_id = 1 
        self.creator_user_id = self.user.id
        self.file_group = FileGroup.objects.create(name = 'fileGroup')
        self.file_extension = FileExtension.objects.create(name = 'fileExtension')
        self.file_type = FileType.objects.create(name = 'file') 
        self.file_type.file_extension.add(self.file_extension)
        
        #Platzhalter-Bild erstellen
        image = Image.new("RGB", (100, 100), color="red")
        image_bytes = BytesIO()
        image.save(image_bytes, format="PNG")
        self.image_data = image_bytes.getvalue()

        #Platzhalter-Bild erstellen für update
        image = Image.new("RGB", (100, 100), color="blue")
        image_bytes = BytesIO()
        image.save(image_bytes, format="PNG")
        self.image_data_updated = image_bytes.getvalue()

        kwargs = {
                'file_type': self.file_type,
                'data' : self.image_data,
                'file_group': self.file_group,
                'name' : self.file_group.name
            }
        self.file_manager_obj = FileManager.create(self.creator_user_id, **kwargs)

    def test_create(self):
        kwargs = {
            'file_type': self.file_type,
            'data' : self.image_data,
            'file_group': self.file_group,
            'name' : self.file_group.name
        }
        file_manager_obj = FileManager.create(self.creator_user_id, **kwargs)

        self.assertIsInstance(file_manager_obj, FileManager)
        
        obj = File.objects.get(id=file_manager_obj.id)
        self.assertEqual(obj.data, file_manager_obj.data)  
        self.assertEqual(obj.file_type.id, self.file_type.id)
        self.assertEqual(obj.file_group.id, 3)
    
    def test_update(self): 
        update = {
            'data': self.image_data_updated,   
        }
        file_manager = FileManager(self.file_manager_obj.file_group)
        file_manager.update(self.creator_user_id, **update)

        updated_obj = File.objects.latest('id')
        self.assertEqual(updated_obj.data, self.image_data_updated)

    def test_deactivate(self):
        file_manager = FileManager(self.file_manager_obj.file_group)
        obj = File.objects.get(id=self.file_manager_obj.id)
        self.assertTrue(obj.active)

        file_manager.deactivate(self.creator_user_id)
        deactivated_obj = File.objects.latest('id')
        self.assertFalse(deactivated_obj.active)
   
    def test_filter(self):
        filter_kwargs = {
            'data': self.image_data,
        }
        result = FileManager.filter(**filter_kwargs)
        expected_result = [
            FileManager(file_group_id=self.file_manager_obj.file_group) 
        ]
        self.assertEqual(result, expected_result)