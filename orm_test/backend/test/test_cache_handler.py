from django.test import TestCase
from unittest.mock import Mock, patch
from backend.models import CacheIntermediate
from backend.src.auxiliary.cache_handler import Watcher, CacheHandler
from datetime import datetime
import pickle


class TestWatcher(TestCase):
    
    def setUp(self):
        # Mocking dependency object
        self.dependency_mock = Mock()
        self.dependency_mock.identification_dict = {'id': 1}

        self.watcher = Watcher(self.dependency_mock)

    def test_add_dependent_object(self):
        obj_mock = Mock()
        self.watcher.addDependentObject(obj_mock)
        self.assertIn(obj_mock, self.watcher.dependent_object_list)

    def test_inform(self):
        obj_mock1 = Mock()
        obj_mock2 = Mock()

        self.watcher.addDependentObject(obj_mock1)
        self.watcher.addDependentObject(obj_mock2)

        self.watcher.inform()
        
        obj_mock1.setEndDate.assert_called_once()
        obj_mock2.setEndDate.assert_called_once()

    def test_destroy(self):
        cache_handler_mock = Mock()
        with patch.object(CacheHandler, 'removeWatcher', new=cache_handler_mock):
            self.watcher.destroy()
        cache_handler_mock.assert_called_once_with(self.watcher.identification)


class TestCacheHandler(TestCase):

    def setUp(self):
        self.dependency_mock = Mock()
        self.dependency_mock.identification_dict = {'id': 1}
        self.cache_handler = CacheHandler()

    def test_add(self):
        obj_mock = Mock()
        obj_mock.dependencies = [self.dependency_mock]

        with patch.object(CacheHandler, '_CacheHandler__getOrCreateWatcher', return_value=Mock()) as get_or_create_watcher_mock:
            self.cache_handler.add(obj_mock)
        get_or_create_watcher_mock.assert_called_once_with(self.dependency_mock)

    # def test_update(self):
    #     obj_mock = Mock()
    #     watcher_mock = Mock()

    #     with patch.object(CacheHandler, '_CacheHandler__getOrCreateWatcher', return_value=watcher_mock):
    #         self.cache_handler.update(obj_mock)
    #     watcher_mock.assert_called_once()

    def test_remove_watcher(self):
        identification = 'identification'
        self.cache_handler.watch_dict[identification] = Mock()
        self.cache_handler.removeWatcher(identification)
        self.assertNotIn(identification, self.cache_handler.watch_dict)

    # def test_start_up_cache_handler(self):
    #     # Assuming CacheIntermediate has a manager called objects
    #     with patch.object(CacheIntermediate.objects, 'filter', return_value=[Mock()]) as filter_mock:
    #         with patch.object(CacheHandler, 'add') as add_mock:
    #             self.cache_handler._CacheHandler__startUpCacheHandler()
        
    #     filter_mock.assert_called_once_with(end_date__isnull=True)
    #     add_mock.assert_called_once()
