
from backend.models import DerivativeConstelliumGroup, DerivativeConstellium
from backend.src.auxiliary.manager import GeneralManager


class DerivativeConstelliumManager(GeneralManager):
    """
    A manager class for handling DerivativeConstellium-related operations, 
    extending the GeneralManager.

    Attributes:
        group_model (models.Model): The DerivativeConstelliumGroup model.
        data_model (models.Model): The DerivativeConstellium model.
    """
    group_model = DerivativeConstelliumGroup
    data_model = DerivativeConstellium

    def __init__(
            self, 
            derivative_constellium_group_id, 
            search_date=None, 
            use_cache=True
            ):
        """
        Initialize a DerivativeConstelliumManager instance.

        Args:
            derivative_constellium_group_id (int): 
                The ID of the DerivativeConstelliumGroup instance.
            search_date (datetime.datetime, optional): 
                The date used for filtering data. Defaults to None.
            use_cache (bool, optional): 
                Whether to use the cache for data retrieval. Defaults to True.
        """
        derivative_constellium_group, derivative_constellium = super().__init__(
            group_id=derivative_constellium_group_id,
            search_date=search_date
        )
        self.project_group_id = derivative_constellium_group.project_group.id
        self.name = derivative_constellium.name
        self.sop_date = derivative_constellium.sop_date
        self.eop_date = derivative_constellium.eop_date
        self.location = derivative_constellium.location
        self.derivative_type = derivative_constellium.derivative_type
        self.estimated_price = derivative_constellium.estimated_price
        self.estimated_weight = derivative_constellium.estimated_weight
        self.prediction_accuracy = derivative_constellium.prediction_accuracy
        self.file_group_id = derivative_constellium.file_group.id
        self.derivative_constellium_group = derivative_constellium_group.id

    @property
    def project_manager(self):
        """
        Get a ProjectManager instance for the 
        current DerivativeConstelliumManager.

        Returns:
            ProjectManager: An instance of the ProjectManager class.
        """
        from project_manager import ProjectManager
        return ProjectManager(self.project_group_id, self.search_date)

    @property
    def file(self):
        """
        Get a File instance for the current DerivativeConstelliumManager.

        Returns:
            FileManager: An instance of the FileManager class.
        """
        from file_manager import FileManager
        return FileManager(self.file_group_id, self.search_date) 
    
