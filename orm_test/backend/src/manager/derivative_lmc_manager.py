if __name__ == '__main__':
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'orm_test.settings')

    import django
    django.setup()

from backend.models import DerivativeLMCGroup, DerivativeLMC
from backend.src.auxiliary.manager import GeneralManager


class DerivativeLmcManager(GeneralManager):
    group_model = DerivativeLMCGroup
    data_model = DerivativeLMC

    def __init__(self, derivative_lmc_group_id: int, search_date=None, use_cache=True):
        derivative_group, derivative = super().__init__(
            group_id=derivative_lmc_group_id,
            search_date=search_date
        )

        self.lmc_full_code = derivative.lmc_derivative_group.lmc_full_code
        self.lmc_model_code = derivative.lmc_derivative_group.lmc_model_code
        self.region = derivative.region
        self.trade_region = derivative.trade_region
        self.country = derivative.country
        self.sales_group = derivative.sales_group
        self.manufacturer = derivative.manufacturer
        self.local_make = derivative.local_make
        self.local_model_line = derivative.local_model_line
        self.local_program_code = derivative.local_program_code
        self.local_production_model = derivative.local_production_model
        self.global_make = derivative.global_make
        self.global_production_model = derivative.global_production_model
        self.gvw = derivative.gvw
        self.platform = derivative.platform
        self.plant = derivative.plant
        self.production_type = derivative.production_type
        self.vehicle_type = derivative.vehicle_type
        self.regional_size = derivative.regional_size
        self.regional_body_type = derivative.regional_body_type
        self.regional_status = derivative.regional_status
        self.global_size = derivative.global_size
        self.global_body_type = derivative.global_body_type
        self.global_status = derivative.global_status
        self.sop_date = derivative.sop_date
        self.eop_date = derivative.eop_date
        self.next_facelift = derivative.next_facelift
        self.last_actual = derivative.last_actual
        self.design_lead = derivative.design_lead
        self.design_lead_location = derivative.design_lead_location
        self.design_lead_country = derivative.design_lead_country

    # @property
    # def derivative_volume_list(self):
    #     from derivative_volume_manager import DerivativeVolumeLmcManager
    #     return DerivativeVolumeLmcManager.filter(
    #         date=self.search_date,
    #         derivative_group_id=self.group_id
    #     )

DerivativeLmcManager(1)