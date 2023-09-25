from backend.src.manager import DerivativeConstelliumManager, DerivativeLmcVolumeManager
from backend.src.auxiliary.intermediate import GeneralIntermediate
from datetime import datetime

class VolumeLmcDerivativeConstelliumIntermediate(GeneralIntermediate):
    relevant_scenario_keys = [] #lmc revision, customer volume increase, lmc car volume increase

    def __init__(
        self,
        derivative_constellium_group_id: int,
        search_date: datetime | None = None,
        scenario_dict: dict = {},
    ):

        self.derivative_constellium_manager = DerivativeConstelliumManager(
            group_id=derivative_constellium_group_id,
            search_date=search_date,
        )

        self.current_volume = self.getCurrentVolume()

        self.super().__init__(
            search_date,
            scenario_dict,
        )

    def getCurrentVolume(self):
        total_volume = {}
        for extension_data in self.derivative_constellium_manager.derivative_constellium_derivative_lmc_connection:
            derivative_lmc_group_id = extension_data['derivative_lmc_group_id']
            der_lmc_volume = DerivativeLmcVolumeManager(derivative_lmc_group_id)
            current_lmc_volume = der_lmc_volume.current_volume
            for datum, volume in current_lmc_volume:
                if datum not in total_volume:
                    total_volume[datum] = 0
                total_volume[datum] += volume*extension_data['take_rate']
