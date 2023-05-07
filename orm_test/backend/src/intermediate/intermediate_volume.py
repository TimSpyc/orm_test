if __name__ == '__main__':
    import sys
    import os

    # sys.path.append(r'C:\Users\Spyc\Django_ORM')
    sys.path.append(r'C:\Users\Spyc\Django_ORM\orm_test')
    # sys.path.append(r'C:\Users\Spyc\Django_ORM\orm_test\orm_test')
    # sys.path.append(r'C:\Users\Spyc\Django_ORM\orm_test\backend\src\manager')
    # sys.path.append(r'C:\Users\Spyc\Django_ORM\orm_test\backend\src\auxiliary')
    # sys.path.append(r'C:\Users\Spyc\Django_ORM\orm_test\backend')
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'orm_test.settings')

    import django
    django.setup()

import pickle
from backend.src.manager.derivative_lmc_manager import DerivativeLmcManager
from backend.src.manager.derivative_volume_manager import DerivativeLmcVolumeManager
from backend.models import CacheIntermediate
from backend.src.auxiliary.meta_class import UpdateCacheAttributeChangeMeta


class GeneralIntermediate(metaclass=UpdateCacheAttributeChangeMeta):
    manager_dependencies: list
    intermediate_dependencies: list
    scenario_keys: list

    __intermediate_name = None
    __intermediate_dependencies = None
    __intermediate_relevant_scenario_dict = None

    def __new__(cls, use_cache=True, search_date=None, **kwargs):
        print('__new__ parent class')
        if hasattr(cls, "_from_cache"):
            return super().__new__(cls) 

        dependencies_dict = {}

        for dependency in cls.manager_dependencies:
            manager_name, group_date_tuple = cls.__getManagerDependency(dependency, kwargs)
            dependencies_dict[manager_name] = group_date_tuple
        
        for dependency in cls.intermediate_dependencies:
            intermediate = dependency['class']            
            dependencies_dict[intermediate.__name__] = manager(**{
                cls.createFilterDict(dependency['filter'], {**kwargs})
            })

        scenario_dict = {}

        cls.__intermediate_name = cls.__name__
        cls.__intermediate_dependencies = cls.getDependenciesAsId(dependencies_dict)
        cls.__intermediate_relevant_scenario_dict = cls.extractItems(scenario_dict, cls.scenario_keys)

        if use_cache:
            result = CacheIntermediate.object.filter(
                intermediate_name = cls.__intermediate_name,
                dependencies = cls.__intermediate_dependencies,
                relevant_scenario_dict = cls.__intermediate_relevant_scenario_dict,
            )

            if result.exists():
                entry = result.first()
                instance =  pickle.loads(entry.data)
                instance._from_cache = True
                return instance

        instance = super().__new__(cls)
        instance.__init__(kwargs)
        instance.__dependencies_dict = dependencies_dict
        instance._from_cache = False

        return instance
        
    def __init__(self, **kwargs):
        print('__init__ parent class')
        pass

        # return dependencies

    def updateCache(self):
        if self.use_cache:
            entry = CacheIntermediate.object.get_or_create(
                intermediate_name = self.__intermediate_name,
                dependencies = self.__intermediate_dependencies,
                relevant_scenario_dict = self.__intermediate_relevant_scenario_dict,
            )

            entry.data=pickle.dumps(self)
            entry.save()

    @staticmethod
    def __getIntermediateDependency(dependency, all_search_kwargs):
        intermediate = dependency['class']
        needed_kwargs = dependency['filter']
        GeneralIntermediate.__createFilterDict(needed_kwargs, all_search_kwargs)
        intermediate_obj_list = intermediate

        manager_name = manager.__name__
        group_date_tuple = [
            (manager_obj.group_id, manager_obj.date)
            for manager_obj in manager_obj_list
        ]

        return manager_name, group_date_tuple

    @staticmethod
    def __getIntermediateObjectList(manager, all_search_kwargs, needed_kwargs):
        filter_dict = 
        return manager.filter(filter_dict)

    @staticmethod
    def __getManagerDependency(dependency, all_search_kwargs):
        manager = dependency['class']
        needed_kwargs = dependency['filter']
        manager_obj_list = GeneralIntermediate.__getManagerObjectList(manager, all_search_kwargs, needed_kwargs)

        manager_name = manager.__name__
        group_date_tuple = [
            (manager_obj.group_id, manager_obj.date)
            for manager_obj in manager_obj_list
        ]

        return manager_name, group_date_tuple

    @staticmethod
    def __getManagerObjectList(manager, all_search_kwargs, needed_kwargs):
        filter_dict = GeneralIntermediate.__createFilterDict(needed_kwargs, all_search_kwargs)
        return manager.filter(filter_dict)


    @staticmethod
    def getDependenciesAsId(dependencies_dict: dict) -> dict:
        dependencies_id_dict = {}
        for dependency_name, dep_obj_list in dependencies_dict.items():
            dependencies_id_dict[dependency_name] = [
                obj.id for obj in dep_obj_list
            ]
        return dependencies_id_dict

    @staticmethod
    def extractItems(data_dict: dict, keys_list: list) -> dict:
        result = {}
        for key in keys_list:
            result[key] = data_dict.get(key, None)
        return result

    @staticmethod
    def __createFilterDict(needed_kwargs: list, all_search_kwargs: dict) -> dict:
        filter_dict = {}
        for var in needed_kwargs:
            if var not in all_search_kwargs.keys():
                raise ValueError(
                    f'''
                        The value {var} you have defined as search value is not
                        inside of your kwargs: 
                        ({' ,'.join([k for k in all_search_kwargs.keys()])})
                    '''
                )
            filter_dict[var]=all_search_kwargs[var]
        
        return filter_dict

class LmcVolumeIntermediate(GeneralIntermediate):
    manager_dependencies = [
        {
            'class': DerivativeLmcManager,
            'filter': {
                'derivative_lmc_group_id': 'derivative_lmc_group_id',
                'search_date': 'search_date'
            }
        },
        {
            'class': DerivativeLmcVolumeManager,
            'filter': {
                'derivative_lmc_group_id': 'derivative_lmc_group_id',
                'search_date': 'search_date'
            }
        },
    ]
    intermediate_dependencies = []
    scenario_keys = ['lmc_volume_percentage', 'lmc_volume_absolute']

    def __init__(self, derivative_lmc_group_id, scenario_id = None, search_date=None, use_cache=True):
        print('__init__ child class')
        
        dependencies = super().__init__(
            derivative_lmc_group_id=derivative_lmc_group_id,
            search_date=search_date
        )

        self._volume = None
        self.derivative_lmc_manager = dependencies['DerivativeLmcManager'][0]
        self.derivative_lmc_volume_manager_list = dependencies['DerivativeLmcVolumeManager']
        self.lmc_rev = None

    @property
    def volume(self):
        if self._volume is None:
            pass

        return self._volume


LmcVolumeIntermediate(1)
print('test')