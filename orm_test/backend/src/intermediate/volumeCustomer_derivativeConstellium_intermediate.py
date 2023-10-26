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
        # There is no test needed for this function,
        # because it is only a wrapper for the
        # CustomerVolumeManager.filter function.        
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

        Declare:
        --------
        self.volume_manager_list : list of CustomerVolumeManager objects
            The filtered list of customer volume managers.
        self.volume_manager : CustomerVolumeManager object
            The customer volume manager with the current volume.

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
    
# 1. wir finden genau einen Manager! -> alles gut
# 2. wir finden keinen Manager -> leere Liste
# 3. wir finden mehr als einen Manager -> Fehler
