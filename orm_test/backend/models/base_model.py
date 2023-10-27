# Responsible Maximilian Kelm
from django.db import models
from django.db.models.fields import NOT_PROVIDED
from django.core.exceptions import ValidationError

# TODO: Check if there is only one validator per field
class BaseModel(models.Model):
    validator_list = NOT_PROVIDED

    def clean(self) -> None:
        if self.validator_list == NOT_PROVIDED\
        or not self.validator_list:
            return

        validation_error_list = []

        for custom_validator_obj in self.validator_list:
            try:
                custom_validator_obj(self).validate()
            except ValidationError as e:
                validation_error_list.append(e)
            except Exception as e:
                raise e          

        if validation_error_list:
            raise ValidationError(validation_error_list)

    class Meta:
        abstract = True