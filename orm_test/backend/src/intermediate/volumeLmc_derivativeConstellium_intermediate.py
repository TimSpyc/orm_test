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
        """
        Description:
        --------
        Get the total volume of all derivative LMC groups based on the
        derivative_constellium_derivative_lmc_connection_list_of_dict.

        Declare:
        --------
        total_volume : list of dictionaries
            The total volume of all derivative LMC groups.
        extension_data : dictionary
            The extension data of the derivative constellium derivative LMC connection dictionary list.
        derivative_lmc_group_id : int
            The ID of the derivative LMC group.
        der_lmc_volume : DerivativeLmcVolumeManager object
            The derivative LMC volume manager.
        current_lmc_volume : list of dictionaries
            The current LMC volume of the derivative LMC volume manager.
        volume_data : dictionary
            The volume data of the current LMC volume.
        datum : datetime object
            The date of the volume data.
        volume : float
            The volume of the volume data.
        existing_volume : dictionary
            The existing volume data with the same date as the current volume data.

        Returns:
        --------
        total_volume : list of dictionaries
            The total volume of all derivative LMC groups.
        """
        total_volume = []
        for extension_data in self.derivative_constellium_manager.\
            derivative_constellium_derivative_lmc_connection_list_of_dict:
            derivative_lmc_group_id = extension_data['derivative_lmc_group'].id
            der_lmc_volume = DerivativeLmcVolumeManager(
                group_id=derivative_lmc_group_id,
                search_date=self.search_date
            )
            print('der_lmc_volume.current_volume', der_lmc_volume.current_volume)
            current_lmc_volume = der_lmc_volume.current_volume

            for volume_data in current_lmc_volume:
                datum = volume_data['volume_date']
                volume = volume_data['volume']

                existing_volume = next(
                    (v for v in total_volume if v['date'] == datum), None
                )
                if existing_volume:
                    existing_volume['volume'] += \
                        volume * extension_data['take_rate']
                else:
                    total_volume.append({
                        'date': datum,
                        'volume': volume * extension_data['take_rate']
                    })
        return total_volume

