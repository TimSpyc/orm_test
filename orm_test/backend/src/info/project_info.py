# Responsible Maximilian Kelm
from backend.src.auxiliary.info_handler import addPrefixToDict
from backend.src.manager import ProjectManager

def serializeProject(
    project_manager_obj: ProjectManager
) -> dict:

    return {
        **dict(project_manager_obj), 
    }