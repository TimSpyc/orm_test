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

import pickle
from backend.src.manager.derivative_lmc_manager import DerivativeLmcManager
from backend.src.manager.derivative_volume_manager import DerivativeLmcVolumeManager
from backend.models import CacheIntermediate
from backend.src.auxiliary.meta_class import UpdateCacheAttrubuteChangeMeta


class GeneralIntermediate(metaclass=UpdateCacheAttrubuteChangeMeta):
    manager_dependencies: list
    intermediate_dependencies: list
    scenario_keys: list = []

    __intermediate_name = None
    __intermediate_dependencies = None
    __intermediate_relevant_scenario_dict = None

    def __new__(cls, scenario_dict = {}, use_cache=True, search_date=None, **kwargs):

        if hasattr(cls, "_from_cache"):
            return super().__new__(cls) 

        dependencies_dict = {}
        for dependency in cls.manager_dependencies:
            manager = dependency['class']            
            dependencies_dict[manager.__name__] = manager(**{
                createFilterDict(dependency['filter'], kwargs)
            })

        for dependency in cls.intermediate_dependencies:
            intermediate = dependency['class']            
            dependencies_dict[intermediate.__name__] = manager(**{
                createFilterDict(dependency['filter'], kwargs)
            })

        cls.__intermediate_name = cls.__name__
        cls.__intermediate_dependencies = cls.getDependenciesAsId(dependencies_dict)
        cls.__intermediate_relevant_scenario_dict = extractItems(scenario_dict, scenario_keys)

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


        return dependencies

    def updateCache(self):
        if self.use_cache:
            entry = CacheIntermediate.object.get_or_create(
                intermediate_name = cls.__intermediate_name,
                dependencies = cls.__intermediate_dependencies,
                relevant_scenario_dict = cls.__intermediate_relevant_scenario_dict,
            )

            entry.data=pickle.dumps(data)
            entry.save()

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
    def createFilterDict(filter_var_list: list, **kwargs: dict) -> dict:
        filter_dict = {}
        for var in filter_var_list:
            if var not in kwargs.keys():
                raise ValueError(
                    f'''
                        The value {var} you have defined as search value is not
                        inside of your kwargs: 
                        ({' ,'.join([k for k in kwargs.keys()])})
                    '''
                )
            filter_dict[var]=kwargs[var]
        
        return filter_dict

class LmcVolumeIntermediate(GeneralIntermediate):
    manager_dependencies = [
        {
            'class': DerivativeLmcManager,
            'filter': {
                'derivative_group_id': 'derivative_lmc_group_id',
                'search_date': 'search_date'
            }
        },
        {
            'class': DerivativeLmcVolumeManager,
            'filter': {
                'derivative_group_id': 'derivative_lmc_group_id',
                'search_date': 'search_date'
            }
        },
    ]
    intermediate_dependencies = []
    scenario_keys = ['lmc_volume_percentage', 'lmc_volume_absolute']

    def __init__(self, derivative_lmc_group_id, search_date=None, use_cache=True):
        
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



