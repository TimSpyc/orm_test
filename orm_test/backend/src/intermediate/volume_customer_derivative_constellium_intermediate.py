# Responsible Elias Bauer

from backend.models import CustomerVolumeGroup
from backend.src.manager import DerivativeConstelliumManager, CustomerVolumeManager
from backend.src.auxiliary.intermediate import GeneralIntermediate
from datetime import datetime

class VolumeCustomerDerivativeConstelliumIntermediate(GeneralIntermediate):
    relevant_scenario_keys = [] #customer revision, customer volume increase, customer car volume increase

    def __init__(
        self,
        derivative_constellium_group_id: int,
        search_date: datetime | None = None,
        scenario_dict: dict = {},
    ):
        self.search_date = search_date
        self.volume = self.getVolume(derivative_constellium_group_id)

        super().__init__(
            search_date,
            scenario_dict,
        )

    def getVolume(self, derivative_constellium_group_id):
        self.volume_manager_list = CustomerVolumeManager.filter(
            derivative_constellium_group_id=derivative_constellium_group_id,
            search_date=self.search_date,
            active=True,
            used_volume=True
        )
        if len(self.volume_manager_list) != 1:
            raise ValueError(f'Expected exactly one customer volume manager, but got {len(self.volume_manager_list)}')
        self.volume_manager = self.volume_manager_list[0]
        self.current_volume = self.volume_manager.current_volume
