# Responsible Maximilian Kelm
from typing import Any, Dict, List
from django.db import models
from django.db.models.fields import NOT_PROVIDED
from django.core.exceptions import ValidationError
from backend.src.auxiliary.exceptions import (
    NotImplementedYet,
    NotConfigured,
)

class NOT_CONFIGURED:
    pass

def checkValidatorConfigured(func):
    def wrapper(self, *args, **kwargs):
        error_list = []
        if self.model_obj == NOT_CONFIGURED:
            error_list.append(
                "There is no model object assigned to the validator"
            )
        if self.message == NOT_CONFIGURED:
            error_list.append("The message for the validator is not configured")

        if error_list:
            raise NotConfigured(error_list)

        return func(self, *args, **kwargs)
    return wrapper

class BaseCustomValidator:
    message = NOT_CONFIGURED

    def __init__(self, field_name: str) -> None:
        if not isinstance(field_name, str):
            raise TypeError(
                "The field_name must be defined and of type string!"
            )

        self.field_name = field_name

        self.model_obj = NOT_CONFIGURED
        self.value_to_validate = NOT_CONFIGURED

    def __call__(self, model_obj: models.Model) -> 'BaseCustomValidator':
        # TODO: Model object should be checked!
        # if not isinstance(model_obj, models.base.ModelBase):
        #     raise TypeError(
        #         "The model_obj must be defined and of type ModelBase!"
        #     )

        self.model_obj = model_obj
        self.value_to_validate = self.__getValueToValidate()

        return self

    def __getValueToValidate(self) -> Any:
        return self._getValueFromModelObjectWithFieldName(self.field_name)

    def _getValueFromModelObjectWithFieldName(self, field_name: str) -> Any:
        if hasattr(self.model_obj, field_name):
            return getattr(self.model_obj, field_name)

        raise ValueError(f"""
            The model_obj has no attribute with the given field_name!
            -> model_obj: "{self.model_obj}"
            -> field_name: "{self.field_name}"
        """)

    @checkValidatorConfigured
    def validate(self) -> None:
        raise NotImplementedYet("The validate method must be implemented!")

        # -> Base example for validate method:
        # if not valid_value:
        #     self.__raiseValidationError(params_dict)
        # Or:
        # RegexValidator(
        #     _lazy_re_compile(r"^-?\d+\Z"),
        #     message=_("Enter a valid integer."),
        #     code="invalid",
        # )

    def _raiseValidationError(self, params_dict: Dict[str, str]) -> None:
        # TODO: Adjust code and find out how to set the field name as key!
        raise ValidationError(
            self.message, code=self.field_name, params=params_dict
        )

    @checkValidatorConfigured
    def populate(self) -> Any:
        raise NotImplementedYet("The populate method must be implemented!")

    @staticmethod
    def getValidatorDict(
        validator_list: List['BaseCustomValidator']
    ) -> Dict[str, 'BaseCustomValidator']:
        if validator_list == NOT_PROVIDED:
            return {}

        return {
            validator.field_name: validator for validator in validator_list
        }

    @staticmethod
    def getValidatorFromValidatorListWithFieldName(
        field_name: str,
        validator_list: List['BaseCustomValidator']
    ) -> 'BaseCustomValidator':
        if validator_list == NOT_PROVIDED:
            return NOT_PROVIDED

        for validator in validator_list:
            if validator.field_name == field_name:
                return validator
            
        return NOT_PROVIDED