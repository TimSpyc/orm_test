
from backend.models import ProjectNumber, ProjectGroup, Project
from backend.src.auxiliary.manager import GeneralManager

class ProjectManager(GeneralManager):
    """
    A manager class for handling Project-related operations, 
    extending the GeneralManager.

    Attributes:
        group_model (models.Model): The ProjectGroup model.
        data_model (models.Model): The Project model.
    """
    group_model = ProjectGroup
    data_model = Project

    def __init__(self, project_group_id, search_date=None, use_cache=True):
        """
        Initialize a ProjectManager instance.

        Args:
            project_group_id (int): The ID of the ProjectGroup instance.
            search_date (datetime.datetime, optional): 
                The date used for filtering data. Defaults to None.
            use_cache (bool, optional): 
                Whether to use the cache for data retrieval. Defaults to True.
        """
        project_group, project = super().__init__(
            group_id=project_group_id,
            search_date=search_date
        )

        self.name = project.name
        self.project_number = project.project_number
        self.project_status = project.project_status
        self.project_type = project.project_type
        self.currency = project.currency
        self.file_group_id:  int = project.file_group.id
        self.customer = project.customer
        self.probability_of_nomination = project.probability_of_nomination
        self.project_group = project_group.id


    @property
    def file(self):
        """
        Get a File instance for the current ProjectManager.

        Returns:
            FileManager: An instance of the FileManager class.
        """
        from file_manager import FileManager
        return FileManager(self.file_group_id, self.search_date)  
    

    @staticmethod
    def getOrCreateProjectNumber(project_number: str) -> ProjectNumber:
        return ProjectNumber.objects.get_or_create(
            project_number=project_number
            )
    
    
    def checkIfProjectNumberIdIsAlreadyOccupiedInActiveProject(
        self,    
        project_number, 
    ):
        pass
        
        


