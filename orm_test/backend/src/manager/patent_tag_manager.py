from backend.models import PatentTag, PatentTagGroup
from backend.src.auxiliary.manager import GeneralManager


class PatentTagManager(GeneralManager):
    """
    A manager class for handling PatentTag-related operations, 
    extending the GeneralManager.

    Attributes:
        group_model (models.Model): The PatentTagGroup model.
        data_model (models.Model): The PatentTag model.
    """
    group_model = PatentTagGroup
    data_model = PatentTag

    def __init__(self, patent_tag_group_id, search_date=None, use_cache=True):
        """
        Initialize a PatentTagManager instance.

        Args:
            patent_group_id (int): The ID of the PatentTagGroup instance.
            search_date (datetime.datetime, optional): 
                The date used for filtering data. Defaults to None.
            use_cache (bool, optional): 
                Whether to use the cache for data retrieval. Defaults to True.
        """
        patent_tag_group, patent_tag = super().__init__(
            group_id=patent_tag_group_id,
            search_date=search_date
        )
        self.text = patent_tag.text 
        self.alt_text1 = patent_tag.alt_text1
        self.alt_text2 = patent_tag.alt_text2
        self.alt_text3 = patent_tag.alt_text3
        self.alt_text4 = patent_tag.alt_text4
        self.alt_text5 = patent_tag.alt_text5
        self.priority_date = patent_tag.priority_date
        self.patent_tag_group = patent_tag_group.id