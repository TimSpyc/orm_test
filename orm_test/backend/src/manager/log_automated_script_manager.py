from django.db import models
from backend.models import ReferenceTable, GroupTable, DataTable
from backend.src.auxiliary.manager import GeneralManager
from datetime import datetime

    
class LogAutomatedScriptGroup(GroupTable):
    script_name = models.CharField(max_length=255)
    script_description = models.TextField()
    execution_interval = models.ForeignKey('LogAutomatedScriptExecutionInterval', on_delete=models.DO_NOTHING)
    responsible_user = models.ForeignKey('User', on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.script_name}"

    @property
    def manager(self):
        return LogAutomatedScriptManager

class LogAutomatedScript(DataTable):
    script_group = models.ForeignKey('LogAutomatedScriptGroup', on_delete=models.DO_NOTHING)
    notification = models.TextField()
    success = models.BooleanField()

    def __str__(self):
        return f"{self.script_name}"
    
    @property
    def group_object(self):
        return self.script_group


class LogAutomatedScriptManager(GeneralManager):
    
    group_model = LogAutomatedScriptGroup
    data_model = LogAutomatedScript
    data_extension_model_list = []