# Responsible Maximilian Kelm
from backend.models.validators.validator import BaseCustomValidator
from backend.models.populate import BasePopulate
from datetime import datetime, timedelta, date, time
from django.utils.translation import gettext_lazy as _
from django.db.models import (
    DateTimeField,
    DateField,
    TimeField
)

class CompareDateTimeValidator(BaseCustomValidator):
    message = _(
        "Ensure %(field_name)s is %(comparison)s %(comparison_field_name)s"
    )

    ALLOWED_FIELD_TYPES= [
        DateTimeField,
        DateField,
        TimeField
    ]
    ALLOWED_OPERATOR_DICT = {
        ">" : "greater than",
        ">=": "greater than or equal to",
        "<" : "less than",
        "<=": "less than or equal to",
        "==": "equal to",
    }

    def __init__(
        self,
        model_obj,
        field_name: str,
        comparison_field_name: str,
        comparison_operator: str
    ):
        super().__init__(model_obj, field_name)

        self.comparison_field_name = comparison_field_name
        self.comparison_operator = comparison_operator

        # TODO: Check field names are fields of the model object!
        # TODO: Check field types are in ALLOWED_FIELD_TYPES!
        # TODO: Check both fields are of the same type!
        # TODO: Check comparison_operator is in ALLOWED_OPERATOR_DICT.keys()!

    def validate(self):
        value_to_validate_with = self._getValueFromModelObjectWithFieldName(
            self.comparison_field_name
        )
        # TODO: What if one value is None?
        if eval(
            f"a {self.comparison_operator} b",
            {
                "a": self.value_to_validate,
                "b": value_to_validate_with
            }
        ):
            return
        
        self._raiseValidationError({
            "field_name": self.field_name,
            "comparison": self.ALLOWED_OPERATOR_DICT[self.comparison_operator],
            "comparison_field_name": self.comparison_field_name
        })

    # @staticmethod
    # def populate():
    #     # TODO: Write populate method!