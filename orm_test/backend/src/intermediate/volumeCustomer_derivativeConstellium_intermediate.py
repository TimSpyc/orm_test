# Responsible Elias Bauer

from backend.src.manager import CustomerVolumeManager
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
        """
        Description:
        --------
        Get the current volume of a customer volume manager based on the
        derivative_constellium_group_id, search_date,
        active, and used_volume attributes.

        Inputs/Parameters:
        ------------------
        derivative_constellium_group_id : int
            The ID of the derivative constellium group.

        Raises:
        -------
        ValueError
            If the length of the filtered customer volume manager list is not exactly 1.

        Returns:
        --------
        current_volume : float
            The current volume of the customer volume manager.
        """
        self.volume_manager_list = CustomerVolumeManager.filter(
            derivative_constellium_group_id=derivative_constellium_group_id,
            search_date=self.search_date,
            active=True,
            used_volume=True
        )
        if len(self.volume_manager_list) != 1:
            raise ValueError(f'Expected exactly one customer volume manager, but got {len(self.volume_manager_list)}')
        self.volume_manager = self.volume_manager_list[0]
        return self.volume_manager.current_volume
