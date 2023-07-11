from backend.models import ChangeRequestGroup, ChangeRequest
from backend.src.auxiliary.manager import GeneralManager


class ChangeRequestManager(GeneralManager):
    """
    A manager class for handling DerivativeConstellium-related operations, 
    extending the GeneralManager.

    Attributes:
        group_model (models.Model): The ChangeRequestGroup model.
        data_model (models.Model): The ChangeRequest model.
    """
    group_model = ChangeRequestGroup
    data_model = ChangeRequest

    def __init__(
            self,
            change_request_group_id, 
            search_date=None, 
            use_cache=True
            ):
        """
        Initialize a ChangeRequestManager instance.

        Args:
            change_request_group_id (int): 
                The ID of the ChangeRequestGroup instance.
            search_date (datetime.datetime, optional): 
                The date used for filtering data. Defaults to None.
            use_cache (bool, optional): 
                Whether to use the cache for data retrieval. Defaults to True.
        """
        change_request_group, change_request = super().__init__(
            group_id=change_request_group_id,
            search_date=search_date
        )
        self.project_group_id = change_request_group.project_group.id
        self.change_request_no = change_request_group.change_request_no
        self.derivative_constellium_group_id: int = \
            change_request.derivative_constellium_group.id
        self.customer_part_number = change_request.customer_part_number
        self.customer_part_name = change_request.customer_part_name
        self.description = change_request.description
        self.ECR_number = change_request.ECR_number
        self.customer_approval = change_request.customer_approval
        self.internal_approval = change_request.internal_approval
        self.change_request_group = change_request_group.id
        

    @property
    def project_manager(self):
        """
        Get a ProjectManager instance for the current ChangeRequestManager.

        Returns:
            ProjectManager: An instance of the ProjectManager class.
        """
        from project_manager import ProjectManager
        return ProjectManager(self.project_group_id, self.search_date)

    @property
    def file(self):
        """
        Get a File instance for the current ChangeRequestManager.

        Returns:
            FileManager: An instance of the FileManager class.
        """
        from file_manager import FileManager
        return FileManager(self.file_group_id, self.search_date) 
    
    @property
    def derivative_constellium(self):
        """
        Get a derivative_constellium instance for the 
        current ChangeRequestManager.

        Returns:
            DerivativeConstelliumManager:
                 An instance of the DerivativeConstelliumManager class.
        """
        from derivative_constellium_manager import DerivativeConstelliumManager
        return DerivativeConstelliumManager(
            self.derivative_constellium_group_id,
            self.search_date
            ) 
    
    #  @property
    # def part(self):
    #     """
    #     Get a Part instance for the current ChangeRequestManager.

    #     Returns:
    #         PartManager: An instance of the PartManager class.
    #     """
    #     from part_manager import PartManager
    #     return PartManager(self.part_group_id, self.search_date) 