from typing import Any
from backend.models.validators.validator import (
    BaseCustomValidator,
    checkValidatorConfigured,
)
import exrex
import re
from django.utils.translation import gettext_lazy as _

class RegexValidator(BaseCustomValidator):
    message = _(
        "Ensure %(field_name)s matches regex pattern %(regex_pattern)s "
    )

    def __init__(
        self,
        field_name: str,
        regex_pattern: str,
    ):
        super().__init__(field_name)
        self.__regex_pattern = regex_pattern

    @property
    def regex_pattern(self):
        return self.__regex_pattern

    @checkValidatorConfigured
    def validate(self) -> None:
        if re.match(self.regex_pattern, self.value_to_validate) is None:
            self._raiseValidationError({
                "regex_pattern": self.regex_pattern,
                "field_name": self.field_name,
            })
    
    @checkValidatorConfigured
    def populate(self) -> str:
        return exrex.getone(self.regex_pattern)
