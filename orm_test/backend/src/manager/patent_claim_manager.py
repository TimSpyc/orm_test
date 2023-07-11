from backend.models import PatentClaim, PatentClaimGroup
from backend.src.auxiliary.manager import GeneralManager


class PatentClaimManager(GeneralManager):
    """
    A manager class for handling PatentClaim-related operations, 
    extending the GeneralManager.

    Attributes:
        group_model (models.Model): The PatentClaimGroup model.
        data_model (models.Model): The PatentClaim model.
    """
    group_model = PatentClaimGroup
    data_model = PatentClaim

    def __init__(self, patent_claim_group_id, search_date=None, use_cache=True):
        """
        Initialize a PatentClaimManager instance.

        Args:
            patent_group_id (int): The ID of the PatentClaimGroup instance.
            search_date (datetime.datetime, optional): 
                The date used for filtering data. Defaults to None.
            use_cache (bool, optional): 
                Whether to use the cache for data retrieval. Defaults to True.
        """
        patent_claim_group, patent_claim = super().__init__(
            group_id=patent_claim_group_id,
            search_date=search_date
        )
        self.text = patent_claim.text
        self.patent_group_id: int = patent_claim_group.patent_group.id
        self.patent_claim_group = patent_claim_group.id
      


    @property
    def patent(self):
        """
        Get a Patent instance for the current PatentClaimManager.

        Returns:
            PatentManager: An instance of the PatentManager class.
        """
        from patent_manager import PatentManager
        return PatentManager(self.patent_group_id, self.search_date) 