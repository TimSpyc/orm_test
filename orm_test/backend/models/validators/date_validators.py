# Responsible Maximilian Kelm
from backend.models.validators.validator import (
    BaseCustomValidator,
    checkValidatorConfigured,
    NOT_CONFIGURED
)
from backend.models.populate import BasePopulate
from datetime import datetime, date, time
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.db.models import (
    DateTimeField,
    DateField,
    TimeField
)

class CompareDateTimeValidator(BaseCustomValidator):
    message = _(
        "Ensure %(field_name)s is %(comparison)s %(comparison_field_name)s"
    )

    # TODO: Expand validator to handle all field types defined!
    ALLOWED_FIELD_TYPES = [
        DateTimeField,
        DateField,
        # TimeField,
        # PositiveIntegerField,
        # IntegerField,
        # SmallIntegerField,
        # PositiveSmallIntegerField,
        # BigIntegerField,
        # PositiveBigIntegerField,
        # DecimalField,
        # FloatField,
        # CharField, ?
        # TextField, ?
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
        field_name: str,
        comparison_operator: str,
        comparison_field_name: str,
    ) -> None:
        super().__init__(field_name)

        self.comparison_field_name = comparison_field_name
        self.comparison_operator = comparison_operator

        self.value_to_validate_with = NOT_CONFIGURED

        if self.comparison_operator not in self.ALLOWED_OPERATOR_DICT.keys():
            raise ValueError(f"""
                The comparison operator "{comparison_operator}" is not allowed!
                To show all allowed comparison operators call:
                -> CompareDateTimeValidator.ALLOWED_OPERATOR_DICT
            """)

    def __call__(self, model_obj: models.Model) -> 'CompareDateTimeValidator':
        super().__call__(model_obj)

        field_one = self.model_obj._meta.get_field(self.field_name)
        field_two = self.model_obj._meta.get_field(self.comparison_field_name)
        self.__checkFieldTypeIsAllowed(field_one)
        self.__checkFieldTypeIsAllowed(field_two)
        if type(field_one) != type(field_two):
            raise TypeError(f"""
                The Fields must have same type to be compared!
                -> "{self.field_name}" type({type(self.field_name)})
                -> "{self.comparison_field_name}" type({type(self.comparison_field_name)})
            """)

        self.value_to_validate_with = self._getValueFromModelObjectWithFieldName(
            self.comparison_field_name
        )

        return self

    def __checkFieldTypeIsAllowed(
        self,
        field: DateTimeField | DateField | TimeField
    ) -> None:
        if type(field) not in self.ALLOWED_FIELD_TYPES:
            raise TypeError(f'''
                The field type with the name "{field.name}" is not allowed!
                To show all allowed fields call:
                -> CompareDateTimeValidator.ALLOWED_FIELD_TYPES
            ''')

    def __checkIfValuesAreNone(self) -> bool:
        return self.value_to_validate is None\
            or self.value_to_validate_with is None

    def __evaluateValuesWithOperator(self) -> bool:
        return eval(
            f"value_a {self.comparison_operator} value_b",
            {
                "value_a": self.value_to_validate,
                "value_b": self.value_to_validate_with
            }
        )

    @checkValidatorConfigured
    def validate(self) -> None:
        if self.__checkIfValuesAreNone() or self.__evaluateValuesWithOperator():
            return

        self._raiseValidationError({
            "field_name": self.field_name,
            "comparison": self.ALLOWED_OPERATOR_DICT[self.comparison_operator],
            "comparison_field_name": self.comparison_field_name
        })

    def __populateFieldTypeWithComparisonValue(self) -> datetime | date | time:
        if self.comparison_operator in [">", ">="]:
            attribute_key = "start_date"
        elif self.comparison_operator in ["<", "<="]:
            attribute_key = "end_date"
        else:
            raise ValueError(f"""
                The given comparison operator appears to be unsupported.
                Please check the configuration of the CompareDateTimeValidator!
            """)

        return self.__populateFieldType(
            "Between",
            **{attribute_key: self.value_to_validate_with}
        )

    def __populateFieldType(
        self,
        function_name_ending:str = "",
        **kwargs
    ) -> datetime | date | time:
        field_type = type(self.model_obj._meta.get_field(self.field_name))

        if field_type == DateTimeField:
            value_type = "Datetime"
        elif field_type == DateField:
            value_type = "Date"
        else:
            raise TypeError(f"""
                The given field type appears to be unsupported.
                Please check the configuration of the CompareDateTimeValidator!
            """)

        return BasePopulate.callDefaultPopulateFunction(
            f"{value_type}{function_name_ending}",
            **kwargs
        )

    @checkValidatorConfigured
    def populate(self) -> datetime | date | time:
        if self.value_to_validate_with is None:
            return self.__populateFieldType()

        if self.comparison_operator == "==" or self.comparison_operator\
        in [">=", "<="] and BasePopulate.randomTrue(0.33):
            return self.value_to_validate_with

        return self.__populateFieldTypeWithComparisonValue()