if __name__ == '__main__':
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'orm_test.settings')

    import django
    django.setup()

import pickle
from backend.src.manager.derivative_lmc_manager import DerivativeLmcManager
from backend.src.manager.derivative_volume_manager import DerivativeLmcVolumeManager
from backend.src.auxiliary.intermediate import GeneralIntermediate
from datetime import datetime

class LmcVolumeIntermediate(GeneralIntermediate):

    relevant_scenario_keys = [('volume', 'total')]

    def __init__(
        self,
        derivative_lmc_group_id: int,
        scenario_dict: dict = {},
        search_date: datetime | None = None,
        use_cache: bool = True
    ) -> None:

        self.derivative_lmc_manager = DerivativeLmcManager(
            derivative_lmc_group_id,
            search_date
        )

        # self.derivative_lmc_volume_manager_list = (
        #     DerivativeLmcVolumeManager.filter(
        #         derivative_lmc_group_id = derivative_lmc_group_id
        #     )
        # )

        dependencies = [
            self.derivative_lmc_manager,
            # *self.derivative_lmc_volume_manager_list
        ]
        super().__init__(
            search_date=search_date,
            scenario_dict=scenario_dict,
            dependencies=dependencies
        )


LmcVolumeIntermediate(1)
print('test')