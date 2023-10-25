# Responsible Maximilian Kelm
from typing import Callable, List, Any
from faker import Faker
import random
import json
from datetime import datetime, timedelta, date, time
from decimal import Decimal

from django.db.models import Model
from django.utils.translation import gettext_lazy as _
from django.db.models.fields import NOT_PROVIDED
from django.core.exceptions import ValidationError
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
    MaxLengthValidator,
    MinLengthValidator
)
from django.db.models import (
    IntegerField, 
    PositiveIntegerField, 
    SmallIntegerField, 
    PositiveSmallIntegerField, 
    BigIntegerField, 
    PositiveBigIntegerField, 
    FloatField, 
    DecimalField, 
    DateTimeField, 
    DateField, 
    TimeField, 
    CharField, 
    TextField, 
    EmailField, 
    BooleanField, 
    JSONField
)
from django.db.models.fields.related import (
    ForeignKey,
    # ForeignObject,
    OneToOneField,
    ManyToManyField,
    # ForeignObjectRel,
    ManyToOneRel,
    ManyToManyRel,
    # OneToOneRel,
)

from backend.src.auxiliary.exceptions import (
    IncompatibleValidatorList,
    NotImplementedYet,
    ResultContradictsConfiguration
)

################################################################################
##### base populate class ######################################################
################################################################################

class BasePopulate:
    FAKE = Faker()

    def __init__(self) -> None:
        self.possible_populate_methods = [
            (int, self.createRandomInteger),
            (float, self.createRandomFloat),
            (Decimal, self.createRandomDecimal),
            (str, self.createRandomText),
            (bool, self.createRandomBoolean),
            (datetime, self.createRandomDatetime),
            (date, self.createRandomDate),
            (time, self.createRandomTime)
        ]

        # TODO: There are more methods like dict, list, json, ...

    # ---- Handle data creation methods ----------------------------------------
    @classmethod
    def createRandomInteger(
        cls,
        min_value: int = 0,
        max_value: int = 999999
    ) -> int:
        fake_int: int = cls.FAKE.random_int(min_value, max_value)
        return fake_int

    @staticmethod
    def createRandomFloat(
        min_value: float = 0.0,
        max_value: float = 999999.0
    ) -> float:
        return random.uniform(min_value, max_value)
    
    @staticmethod
    def _createUpperBorderForMaximalDigits(max_digits: int) -> int:
        if max_digits >= 1:
            raise ValueError('must be positive')
        test: int = (10 ** max_digits) - 1
        return test

    @staticmethod
    def createRandomDecimal(
        max_digits: int = 9,
        decimal_places: int = 5
    ) -> Decimal:
        whole_digit = BasePopulate.createRandomInteger(
            0,
            BasePopulate._createUpperBorderForMaximalDigits(
                (max_digits - decimal_places)
            )
        )
        decimal_digit: int | str = BasePopulate.createRandomInteger(
            0,
            BasePopulate._createUpperBorderForMaximalDigits(decimal_places)
        )

        while len(f'{decimal_digit}') < decimal_places:
            decimal_digit = f'0{decimal_digit}'

        return Decimal(f'{whole_digit}.{decimal_digit}')

    @classmethod
    def createRandomDatetime(cls) -> datetime:
        return cls.FAKE.date_time()

    @classmethod
    def createRandomDate(cls) -> date:
        return cls.FAKE.date_object()

    @classmethod
    def createRandomTime(cls) -> time:
        return cls.FAKE.time_object()

    @classmethod
    def createRandomText(cls, min_length: int = 0, max_length: int = 50) -> str:
        # TODO: Check min_chars < max_chars and max_chars-min_chars > 5!
        random_text: str = cls.FAKE.text(max_length)

        while len(random_text) < min_length:
            random_text += cls.FAKE.text(max_length-len(random_text))

        return random_text

    @classmethod
    def createRandomEmail(cls) -> str:
        fake_email: str = cls.FAKE.email()
        return fake_email

    @classmethod
    def createRandomBoolean(
        cls,
        can_be_none: bool = False,
        chance_for_none: float = 0.33
    ) -> bool | None:
        fake_boolean: bool = cls.FAKE.boolean()

        if can_be_none and cls.randomTrue(chance_for_none):
            return None

        return fake_boolean
    
    @classmethod
    def createRandomDict(
        cls,
        max_elements: int = 10,
        min_elements: int = 1,
        # max_depth: int = 3,
        # custom_structure = None
    ) -> dict:
        # TODO: Do we need the possibility to define a custom structure?
        random_data_dict = {}

        for i in range(cls.createRandomInteger(max_elements, min_elements)):
            _, populateValue = cls.randomChoice(cls.possible_populate_methods)
            random_data_dict[f'key_{i}'] = populateValue()

        return random_data_dict
    
    @classmethod
    def createRandomJSON(cls) -> str:
        class MyEncoder(json.JSONEncoder):
            def default(self, obj):
                if isinstance(obj, (datetime, date, time)):
                    return obj.isoformat()
                elif isinstance(obj, Decimal):
                    return str(obj)
                return super().default(obj)

        return json.dumps(cls.createRandomDict(), cls=MyEncoder)

    # ---- ? -------------------------------------------------------------------
    @staticmethod
    def randomTrue(chance_for_true: float) -> bool:
        return chance_for_true > BasePopulate.createRandomFloat(0.0, 1.0)
    
    @staticmethod
    def randomChoice(list_to_select_from: list) -> Any:
        return random.choice(list_to_select_from)

    # ---- Handle custom values ------------------------------------------------
    @staticmethod
    def executeAndReturnValueIfCallable(custom_value: Any) -> bool:
        if isinstance(custom_value, Callable):
            return custom_value()

        return custom_value

    # ---- Handle validator errors ---------------------------------------------
    @staticmethod
    def _checkIntegerDefinition(
        integer: int,
        integer_description: str
    ):
        if not isinstance(integer, int):
            raise ValueError(f'''
                Definition for "{integer_description}" is not an integer!
            ''')

    @staticmethod
    def _checkPercentageDefinition(
        percentage: float,
        percentage_description: str
    ):
        if not isinstance(percentage, float):
            raise ValueError(f'''
                Definition for "{percentage_description}" data is not a float!
            ''')

        if percentage < 0 or percentage > 1:
            raise ValueError(f'''
                Definition for "{percentage_description}" data 
                is not a percentage!
            ''')

    @staticmethod
    def checkOnlyAllowedValidatorsInList(
        validator_list: list,
        allowed_validator_list: list
    ) -> bool:
        return all(
            type(validator) in allowed_validator_list
            for validator in validator_list
        )

    @staticmethod
    def raiseErrorIfValidatorListIsIncompatibleForField(
        field: Any,
        allowed_validator_list: list
    ):
        if not BasePopulate.checkOnlyAllowedValidatorsInList(
            field.validators,
            allowed_validator_list
        ):
            not_supported_validators = [
                type(validator) for validator in field.validators 
                if type(validator) not in allowed_validator_list
            ]

            raise IncompatibleValidatorList(f'''
                The field with the name "{field.name}" contains the following
                validators that are not supported:
                
                {not_supported_validators}

                NOTE: If you want to define more specific validators, please
                customize the clean function of the model!

                Supported validators for this field:
                {allowed_validator_list}
            ''')


################################################################################
##### class to populate fields #################################################
################################################################################

class PopulateField(BasePopulate):
    SUPPORTED_FIELD_LIST = [
        IntegerField,
        PositiveIntegerField,
        SmallIntegerField,
        PositiveSmallIntegerField,
        BigIntegerField,
        PositiveBigIntegerField,
        FloatField,
        DecimalField,
        DateTimeField,
        DateField,
        TimeField,
        CharField,
        TextField,
        EmailField,
        BooleanField,
        JSONField,
        ForeignKey,
        # OneToOneField,
        ManyToManyField
    ]

    def __init__(self, field, **kwargs):
        self.field              = field
        self.custom_populate    = kwargs.get("custom_populate", NOT_PROVIDED)
        self.chance_for_default = kwargs.get("chance_for_default", 0.25)
        self.min_relations      = kwargs.get("min_relations", 1)
        self.max_relations      = kwargs.get("max_relations", 10)

        # TODO: Should there be the possibility to adjust the base type functions?

        self.__checkPopulateFieldDefinitions()

    def __checkPopulateFieldDefinitions(self):
        if type(self.field) not in self.SUPPORTED_FIELD_LIST:
            raise NotImplementedYet(f'''
                The field with the name "{self.field.name}" is not supported yet!
                To show all supported fields call:
                -> PopulateField.SUPPORTED_FIELD_LIST
            ''')

        # TODO: Check custom_populate!
        # -> Therefor the corresponding type of the field is needed...
        # -> Is it enough to test the value before returning it?

        self._checkPercentageDefinition(
            self.chance_for_default,
            "chance_for_default"
        )

        self._checkIntegerDefinition(
            self.min_relations,
            "min_relations"
        )

        self._checkIntegerDefinition(
            self.max_relations,
            "max_relations"
        )

    # ---- Handle data population ----------------------------------------------
    def populate(self) -> Any:
        # TODO: Check if default=null and null=False is possible at model!

        # NOTE: chance_for_default must be set manually to 0.0 if the default
        # is not wanted!
        populated_value = self.__getDefaultValueForFieldRandomly()

        if populated_value == NOT_PROVIDED:
            # TODO: check type of populated value correspond to field type?
            if self.custom_populate != NOT_PROVIDED:
                populated_value = self.executeAndReturnValueIfCallable(
                    self.custom_populate
                )
            else:
                populated_value = self.populateFieldWithDefaultFunction()

        if not self.field.null and populated_value is None:
            raise ValueError(f'''
                The field with the name "{self.field.name}" is not allowed to
                be null! Apparently the configurations of the model and the 
                Populate methods contradict each other.
            ''')

        return populated_value

    def __getDefaultValueForFieldRandomly(self) -> Any:
        if self.randomTrue(self.chance_for_default):
            return self.field.default

        return NOT_PROVIDED

    def populateFieldWithDefaultFunction(self) -> Any:
        try:
            return getattr(self, f"_populate{self.field.__class__.__name__}")()
        except AttributeError:
            raise NotImplementedYet(f'''
                The field "{self.field.name}" with type {type(self.field)} is 
                supported, but no corresponding populate function for 
                "_populate{self.field.__class__.__name__}" can be found! 
                Please check the configuration of the PopulateField class.
            ''')

    # ---- Handle validator logic ----------------------------------------------
    def __getMinMaxValidatorsInfoDict(self, attribute_info_dict: dict) -> dict:
        self.raiseErrorIfValidatorListIsIncompatibleForField(
            self.field,
            attribute_info_dict.keys()
        )

        return {
            attribute_info_dict[type(validator)]: validator.limit_value
            for validator in self.field.validators
            if type(validator) in attribute_info_dict.keys()
        }

    # ---- Handle integer field methods ----------------------------------------
    def __populateIntegerFields(
        self,
        positive_border_value: int,
        only_positive_integer: int = False
    ) -> int:
        negative_border_value = 0
        if not only_positive_integer:
            negative_border_value = (positive_border_value + 1) * -1

        return self.createRandomInteger(
            **{
                "min_value": negative_border_value,
                "max_value": positive_border_value,
                **self.__getMinMaxValidatorsInfoDict({
                    MinValueValidator: "min_value",
                    MaxValueValidator: "max_value"
                })
            }
        )

    def _populateIntegerField(self) -> int:
        return self.__populateIntegerFields(2147483647)

    def _populatePositiveIntegerField(self) -> int:
        return self.__populateIntegerFields(2147483647, True)

    def _populateSmallIntegerField(self) -> int:
        return self.__populateIntegerFields(32767)

    def _populatePositiveSmallIntegerField(self) -> int:
        return self.__populateIntegerFields(32767, True)

    def _populateBigIntegerField(self) -> int:
        return self.__populateIntegerFields(9223372036854775807)

    def _populateBigSmallIntegerField(self) -> int:
        return self.__populateIntegerFields(9223372036854775807, True)

    # ---- Handle float field methods ------------------------------------------
    def _populateFloatField(self) -> float:
        self.raiseErrorIfValidatorListIsIncompatibleForField(self.field, [])

        return self.createRandomFloat()

    # ---- Handle decimal field methods ----------------------------------------
    def _populateDecimalField(self) -> Decimal:
        self.raiseErrorIfValidatorListIsIncompatibleForField(self.field, [])

        selectDefaultForDecimalIfNone: Callable[[int | None], int] =\
            lambda digits: 5 if digits is None else digits

        return self.createRandomDecimal(
            selectDefaultForDecimalIfNone(self.field.max_digits),
            selectDefaultForDecimalIfNone(self.field.decimal_places)
        )

    # ---- Handle datetime field methods ---------------------------------------
    def __populateDateTimeFields(
        self,
        random_datetime: datetime | time | date
    ) -> datetime | time | date | None:
        if self.field.auto_now or self.field.auto_now_add:
            # TODO: Check if return None conflict with other logic! -> YES
            # TODO: Find a way to inform user that value is None/OK if NOT_PROVIDED!
            return None

        self.raiseErrorIfValidatorListIsIncompatibleForField(self.field, [])

        return random_datetime

    def _populateDateTimeField(self) -> datetime | None:
        return self.__populateDateTimeFields(self.createRandomDatetime())

    def _populateDateField(self) -> date | None:
        return self.__populateDateTimeFields(self.createRandomDate())

    def _populateTimeField(self) -> time | None:
        return self.__populateDateTimeFields(self.createRandomTime())

    # ---- Handle text field methods -------------------------------------------
    def __populateTextFields(self) -> str:
        return self.createRandomText(
            **{
                "min_length": 0,
                "max_length": 1000,
                **self.__getMinMaxValidatorsInfoDict({
                    MinLengthValidator: "min_length",
                    MaxLengthValidator: "max_length"
                })
            }
        )

    def _populateCharField(self) -> str:
        return self.__populateTextFields()

    def _populateTextField(self) -> str:
        return self.__populateTextFields()

    # ---- Handle email field methods ------------------------------------------
    def _populateEmailField(self) -> str:
        self.raiseErrorIfValidatorListIsIncompatibleForField(self.field, [])
        if self.field.max_length != 254:
            raise NotImplementedYet(f'''
                The field type EmailField with a max_length other than 254 is 
                not yet supported! Try setting the max_length to 254 or adjust 
                the _populateEmailField function.
            ''')

        return self.createRandomEmail()

    # ---- Handle boolean field methods ----------------------------------------
    def _populateBooleanField(self) -> bool | None:
        self.raiseErrorIfValidatorListIsIncompatibleForField(self.field, [])

        return self.createRandomBoolean(can_be_none=self.field.null)

    # ---- Handle json field methods -------------------------------------------
    def _populateJSONField(self) -> str:
        self.raiseErrorIfValidatorListIsIncompatibleForField(self.field, [])

        return self.createRandomJSON()

    # ---- Handle relationship field methods -----------------------------------
    # TODO: Adjust logic for reference and group tables on PopulateModel!
    def __populateRelationshipFields(
        self,
        relationship_model_list: list[Model]
    ) -> Model:
        if len(relationship_model_list) != 0 and self.randomTrue(0.75):
            return self.randomChoice(relationship_model_list)

        return PopulateModel(self.field.related_model).populate()

    def _populateForeignKey(self) -> Model:
        self.raiseErrorIfValidatorListIsIncompatibleForField(self.field, [])

        if self.field.unique:
            return self._populateOneToOneField()

        return self.__populateRelationshipFields(
            self.field.related_model.objects.all()
        )

    def _populateOneToOneField(self) -> Model:
        # self.raiseErrorIfValidatorListIsIncompatibleForField(self.field, [])

        # -> return self.__populateRelationshipFields(
        #       self.field.related_model.objects.filter(f"{model_name}__isnull"=True)
        # )

        raise NotImplementedYet(f"""
            OneToOneFields (or ForeignKey with unique=True) are currently not 
            supported. As soon as there is a field that meets these conditions, 
            this method must be implemented.
        """)

    def _populateManyToManyField(self) -> list[Model]:
        self.raiseErrorIfValidatorListIsIncompatibleForField(self.field, [])

        many_to_many_list = []
        related_model_list = self.field.related_model.objects.all()

        for _ in range(
            self.createRandomInteger(self.min_relations, self.max_relations)
        ):
            random_model = self.__populateRelationshipFields(related_model_list)
            many_to_many_list.append(random_model)

            if random_model in related_model_list:
                related_model_list.remove(random_model)

        return many_to_many_list


################################################################################
##### class to populate models #################################################
################################################################################

class PopulateModel(BasePopulate):
    # TODO: Check all defined attributes!
    # -> model: check all field types are supported!

    # TODO: wie händle ich die clean methoden?

    def __init__(self, model, **kwargs):
        self.model = model

    def populate(self):
        temp_model = self.model(**{
            field.name: PopulateField(field).populate()
            for field in self.model._meta.get_fields()
            if type(field) in PopulateField.SUPPORTED_FIELD_LIST
        })
        
        temp_model.save()
        
        return temp_model


################################################################################
##### class to populate managers ###############################################
################################################################################

class PopulateManager(BasePopulate):
    pass


################################################################################
##### test section #############################################################
################################################################################
if __name__ == '__main__':
    from backend.models import AssetItem, AssetItemGroup

    # new_model = PopulateModel(AssetItemGroup).populate()
    new_model = PopulateModel(AssetItem).populate()

    print("new_model: ", new_model)

    # test_pop = PopulateField(AssetItem._meta.get_field("max_width")).populate()
    # print("test_pop: ", test_pop)
# PopulateField(AssetItem._meta.get_field("max_width"), custom_populate=lambda: 10).populate()

# new_model = PopulateModel(
#     AssetItem,
#     max_width: Any | Callable | kwargs,
# )

# -> Any: Fixer Wert der dem Typen sowie den Rahmenbedingungen des Feldes entsprechen muss.
# -> Callable: Funktion die einen Wert zurückgibt der dem Typen sowie den Rahmenbedingungen des Feldes entsprechen muss.
# -> kwargs: Die der PopulateField klasse übergeben werden. (ausgeschlossen ist field)