from backend.models import Patent, PatentGroup
from backend.src.auxiliary.manager import GeneralManager


class PatentManager(GeneralManager):
    """
    A manager class for handling Patent-related operations, 
    extending the GeneralManager.

    Attributes:
        group_model (models.Model): The PatentGroup model.
        data_model (models.Model): The Patent model.
    """
    group_model = PatentGroup
    data_model = Patent

    def __init__(self, patent_group_id, search_date=None, use_cache=True):
        """
        Initialize a PatentManager instance.

        Args:
            patent_group_id (int): The ID of the PatentGroup instance.
            search_date (datetime.datetime, optional): 
                The date used for filtering data. Defaults to None.
            use_cache (bool, optional): 
                Whether to use the cache for data retrieval. Defaults to True.
        """
        patent_group, patent = super().__init__(
            group_id=patent_group_id,
            search_date=search_date
        )
        self.remark = patent.remark
        self.abstract = patent.abstract
        self.priority_date = patent.priority_date
        self.patent_number = patent_group.patent_number
        self.patent_group = patent_group.id

    @property
    def patent_claim_list(self):
        from patent_claim_manager import PatentClaimManager
        return PatentClaimManager.filter(patent_group_id= self.group_id)