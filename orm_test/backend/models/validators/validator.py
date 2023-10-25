# Responsible Maximilian Kelm
from typing import Callable, List, Any

from django.db.models.fields import NOT_PROVIDED
from django.core.exceptions import ValidationError

from backend.src.auxiliary.exceptions import (
    IncompatibleValidatorList,
    NotImplementedYet,
    ResultContradictsConfiguration
)

class BaseCustomValidator:
    message = NOT_PROVIDED

    def __init__(self, model_obj, field_name):
        # TODO: Check attributes!
        self.model_obj = model_obj
        self.field_name = field_name
        self.value_to_validate = self.__getValueToValidate()

    def __call__(self):
        self.validate()
    
    def __getValueToValidate(self):
        return self._getValueFromModelObjectWithFieldName(self.field_name)
    
    def _getValueFromModelObjectWithFieldName(self, field_name: str):
        if hasattr(self.model_obj, field_name):
            return getattr(self.model_obj, field_name)
        
        # TODO: Adjust error and msg!
        raise ValueError("The model_obj has no attribute with the given field name!")
        
    def validate(self):
        raise NotImplementedYet("The validate method must be implemented!")

        # -> Base example vor validate method:
        # if not valid_value:
        #     self.__raiseValidationError(params_dict)
        # Or:
        # RegexValidator(
        #     _lazy_re_compile(r"^-?\d+\Z"),
        #     message=_("Enter a valid integer."),
        #     code="invalid",
        # )
    
    def _raiseValidationError(self, params_dict: dict):
        # TODO: Check if params are complete and message is defined!
        raise ValidationError(
            self.message, code=self.field_name, params=params_dict
        )

    @staticmethod
    def populate():
        raise NotImplementedYet("The populate method must be implemented!")