# Responsible Elias Bauer

from backend.src.intermediate import (
    WeightPartIntermediate,
    VolumeLmcDerivativeConstelliumIntermediate,
    VolumeCustomerDerivativeConstelliumIntermediate
)
from backend.src.auxiliary.intermediate import GeneralIntermediate
from datetime import datetime

class ShipmentDerivativeIntermediate(GeneralIntermediate):
    relevant_scenario_keys = []
    
    def __init__(
        self,
        derivative_constellium_group_id: int,
        VolumeDerivativeIntermediateClass: GeneralIntermediate,
        search_date: datetime | None = None,
        scenario_dict: dict = {},
    ):
        
        self.VolumeDerivativeIntermediateClass = VolumeDerivativeIntermediateClass
        self.__checkValidityOfVolumeDerivativeIntermediateClass()

        self.search_date = search_date

        super().__init__(
            search_date,
            scenario_dict,
        )

    def __checkValidityOfVolumeDerivativeIntermediateClass(self):
        if self.VolumeDerivativeIntermediateClass not in [
            VolumeLmcDerivativeConstelliumIntermediate,
            VolumeCustomerDerivativeConstelliumIntermediate
        ]:
            raise ValueError(
                f"{self.VolumeDerivativeIntermediateClass} is not supported"
            )