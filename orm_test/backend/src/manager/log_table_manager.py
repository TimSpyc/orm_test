from django.db import models
from backend.models import ReferenceTable, GroupTable, DataTable
from backend.src.auxiliary.manager import GeneralManager
from datetime import datetime

    
class log__AutomatedScriptGroup(GroupTable):
    script_name = models.CharField(max_length=255)
    script_description = models.TextField()
    execution_interval = models.ForeignKey('log_AutomatedExecutionInterval', on_delete=models.DO_NOTHING)
    responsible_user = models.ForeignKey('User', on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.script_name}"

    @property
    def manager(self):
        return AutomatedScriptManager

class log__AutomatedScript(DataTable):
    script_group = models.ForeignKey('log__AutomatedScriptGroup', on_delete=models.DO_NOTHING)
    notification = models.TextField()
    success = models.BooleanField()

    def __str__(self):
        return f"{self.script_name}"
    
    @property
    def group(self):
        return self.script_group


class AutomatedScriptManager(GeneralManager):
    
    group_model = log__AutomatedScriptGroup
    data_model = log__AutomatedScript
    data_extension_model_list = []

    def __init__(
        self,
        script_group_id:int,
        search_date: datetime | None = None,
        use_cache: bool = True
    ):
        super().__init__(
            group_id=script_group_id,
            search_date=search_date,
            use_cache=use_cache
        )