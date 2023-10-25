# Responsible Elias Bauer

from backend.src.manager import DerivativeConstelliumManager, DerivativeLmcVolumeManager
from backend.src.auxiliary.intermediate import GeneralIntermediate
from datetime import datetime

class VolumeLmcDerivativeConstelliumIntermediate(GeneralIntermediate):
    relevant_scenario_keys = []

    def __init__(
        self,
        derivative_constellium_group_id: int,
        search_date: datetime | None = None,
        scenario_dict: dict = {},
    ):
        self.search_date = search_date
        self.derivative_constellium_manager = DerivativeConstelliumManager(
            group_id=derivative_constellium_group_id,
            search_date=self.search_date,
        )
        

        self.volume = self.getVolume()

        super().__init__(
            search_date,
            scenario_dict,
        )

    def getVolume(self) -> list:
        '''
        Get the current volume for the derivative_constellium_group_id.
        
        Returns:
        --------
         total_volume : list
                A list of dictionaries containing the volume_date and volume.
                Each dictionary has the following keys:
                    - 'volume_date': the date of the volume data (datetime.date object)
                    - 'volume': the volume for the date (float)
        '''
        total_volume = []
        for extension_data in self.derivative_constellium_manager.\
            derivative_constellium_derivative_lmc_connection_dict_list:
            derivative_lmc_group_id = extension_data['derivative_lmc_group'].id
            der_lmc_volume = DerivativeLmcVolumeManager(
                group_id=derivative_lmc_group_id,
                search_date=self.search_date
            )
            current_lmc_volume = der_lmc_volume.current_volume

            for volume_data in current_lmc_volume:
                datum = volume_data['volume_date']
                volume = volume_data['volume']

                existing_volume = next(
                    (v for v in total_volume if v['volume_date'] == datum), None
                )
                if existing_volume:
                    existing_volume['volume'] += \
                        volume * extension_data['take_rate']
                else:
                    total_volume.append({
                        'volume_date': datum,
                        'volume': volume * extension_data['take_rate']
                    })
        return total_volume

