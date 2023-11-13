# Responsible Maximilian Kelm
from typing import Callable, Dict, List, Any
import inspect
from faker import Faker
import random
import json
from datetime import datetime, timedelta, date, time
from decimal import Decimal

from django.db import models
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
    OneToOneRel,
)

from backend.models.validators.validator import BaseCustomValidator, NOT_CONFIGURED
from backend.src.auxiliary.manager import transferToSnakeCase, GeneralManager
from backend.src.auxiliary.exceptions import (
    IncompatibleValidatorList,
    NotImplementedYet,
    ResultContradictsConfiguration
)

################################################################################
##### decorators for populate classes ##########################################
################################################################################

def createTempAttrs(*attr_name_list: list[str]) -> Any:
    def outerWrapper(func):
        def innerWrapper(self, *args, **kwargs) -> Any:
            for attr_name in attr_name_list:
                # TODO: check attr_name name
                setattr(self, attr_name, NOT_CONFIGURED)

            result = func(self, *args, **kwargs)
            
            for attr_name in attr_name_list:
                delattr(self, attr_name)
                
            return result
        return innerWrapper
    return outerWrapper


################################################################################
##### base populate class ######################################################
################################################################################

class BasePopulate:
    FAKE = Faker()

    # TODO: Implement following types dict, list, ...
    SUPPORTED_TYPE_LIST = [
        int,
        float,
        Decimal,
        str,
        bool,
        datetime,
        date,
        time,
    ]

    def __init__(self, type_to_populate: type, **kwargs) -> None:
        self._checkType(type_to_populate, type, "type_to_populate")
        if type_to_populate not in self.SUPPORTED_TYPE_LIST:
            # TODO: adjust error msg
            raise NotImplementedYet(f'''
                The type to populate "{type_to_populate}" is not supported yet!
                To show all supported types call:
                -> BasePopulate.SUPPORTED_TYPE_LIST
            ''')

        self.__type_to_populate = type_to_populate
        self.__populateData = self._getPopulateFuncWithTypeName(
            self.__type_to_populate.__name__
        )

        self._checkAndCreateMetaAttrs(self.__populateData, **kwargs)

    @property
    def type_to_populate(self) -> type:
        return self.__type_to_populate

    # ---- Handle type checks --------------------------------------------------
    @staticmethod
    def _checkType(attr: Any, attr_type: type, attr_name: str) -> None:
        if not isinstance(attr, attr_type):
            raise TypeError(f'''
                The attr "{attr_name}" must be of type "{attr_type}"!
                -> not "{type(attr)}"
            ''')

    @classmethod
    def _checkPercentageDefinition(cls, attr: float, attr_name: str) -> None:
        cls._checkType(attr, float, attr_name)

        if attr < 0 or attr > 1:
            raise ValueError(f'''
                Definition for "{attr_name}" data 
                is not a percentage!
            ''')

    # ---- ? -------------------------------------------------------------------
    @staticmethod
    def randomTrue(chance_for_true: float) -> bool:
        return chance_for_true > BasePopulate.createRandomFloat(0.0, 1.0)
    
    @staticmethod
    def randomChoice(list_to_select_from: list) -> Any:
        return random.choice(list_to_select_from)

    # ---- Select data creation methods ----------------------------------------
    def _getPopulateFuncWithTypeName(self, type_name: str) -> Any:
        function_name =\
            f"createRandom{type_name[:1].capitalize() + type_name[1:]}"

        try:
            return getattr(self, function_name)
        except AttributeError as e:
            raise NotImplementedYet(f'''
                Can't found a corresponding populate function with the name:
                -> {function_name}

                Please check the class configuration for:
                -> {self.__class__.__name__}
            ''')
        except Exception as e:
            raise e

    # ---- Handle data creation methods ----------------------------------------
    @classmethod
    def createRandomInt(
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
        if max_digits < 0:
            raise ValueError('must be positive')
        test: int = (10 ** max_digits) - 1
        return test

    @staticmethod
    def createRandomDecimal(
        max_digits: int = 9,
        decimal_places: int = 5
    ) -> Decimal:
        whole_digit = BasePopulate.createRandomInt(
            0,
            BasePopulate._createUpperBorderForMaximalDigits(
                (max_digits - decimal_places)
            )
        )
        decimal_digit: int | str = BasePopulate.createRandomInt(
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
    def createRandomDatetimeBetween(
        cls,
        start_date:datetime = datetime(1970, 1, 1),
        end_date:datetime = datetime.now()
    ) -> datetime:
        return cls.FAKE.date_time_between(start_date, end_date)

    @classmethod
    def createRandomDate(cls) -> date:
        return cls.FAKE.date_object()

    @classmethod
    def createRandomDateBetween(
        cls,
        start_date:datetime = datetime(1970, 1, 1),
        end_date:datetime = datetime.now()
    ) -> datetime:
        return cls.FAKE.date_between(start_date, end_date)

    @classmethod
    def createRandomTime(cls) -> time:
        return cls.FAKE.time_object()

    @classmethod
    def createRandomStr(cls, min_length: int = 0, max_length: int = 50) -> str:
        if min_length > max_length:
            # TODO adjust error msg
            raise ValueError(f'''
                The min_length "{min_length}" is greater than the max_length
            ''')

        temp_max_length = max_length
        if max_length < 5:
            # TODO: Adjust logic (max_length-min_length)
            temp_max_length = 5
        random_text: str = cls.FAKE.text(temp_max_length)

        while len(random_text) < min_length:
            random_text += cls.FAKE.text(max_length-len(random_text))

        if len(random_text) > max_length:
            random_text = random_text[:-(len(random_text)-max_length)]

        return random_text

    @classmethod
    def createRandomEmail(cls) -> str:
        fake_email: str = cls.FAKE.email()
        return fake_email

    @classmethod
    def createRandomBool(
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
        min_elements: int = 1,
        max_elements: int = 10,
    ) -> dict:
        random_data_dict = {}

        for i in range(cls.createRandomInt(min_elements, max_elements)):
            type_to_populate = cls.randomChoice(cls.SUPPORTED_TYPE_LIST)
            random_data_dict[f'key_{i}'] = cls(type_to_populate).populate()

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

    # ---- handle meta attributes ----------------------------------------------
    @staticmethod
    def _createMetaAttrName(custom_attr_name: str) -> str:
        return f"meta__{custom_attr_name}"

    @classmethod
    def _createMetaAttrListForFunc(cls, func: callable) -> list:
        return [
            cls._createMetaAttrName(attr_name) 
            for attr_name in inspect.signature(func).parameters.keys()
        ]

    def _checkAndCreateMetaAttrs(self, func: callable, **kwargs) -> None:
        possible_meta_attr_list = self._createMetaAttrListForFunc(func)

        for meta_attr, custom_attr in kwargs.items():
            if meta_attr not in possible_meta_attr_list:
                # TODO: adjust error msg
                raise ValueError(f'''
                    The meta attribute with the name "{meta_attr}" is not 
                    allowed!
                ''')
            
            setattr(self, meta_attr, custom_attr)
            
    def _createCustomAttrDict(self, func: callable) -> dict:
        possible_meta_attr_list = self._createMetaAttrListForFunc(func)

        return {
            meta_attr_name[6:]: getattr(self, meta_attr_name)
            for meta_attr_name in possible_meta_attr_list
            if hasattr(self, meta_attr_name)
        }
    
    def _checkCustomAndMetaAttrs(
        self,
        allowed_attr_name_list: list[str],
        **kwargs
    ) -> None:
        allowed_meta_attr_name_list = [
            self._createMetaAttrName(attr_name)
            for attr_name in allowed_attr_name_list
        ]

        for attr_name, attr in kwargs.items():
            if attr_name not in allowed_attr_name_list\
            and attr_name not in allowed_meta_attr_name_list:
                # TODO: adjust error and msg
                print("attr_name", attr_name)
                raise ValueError("Attribute is not allowed")

            # NOTE: If attr_name exists as an attribute will be checked when 
            # creating the custom attribute

            # NOTE: If attr_name in allowed_attr_name_list the type will be 
            # checked when calling the corresponding class

            if attr_name in allowed_meta_attr_name_list\
            and not isinstance(attr, dict):
                # TODO: adjust error msg
                raise TypeError("Meta attribute must be of type dict")

    def _createCustomAndMetaAttrs(
        self,
        allowed_attr_name_list: list[str],
        **kwargs
    ) -> None:
        self._checkCustomAndMetaAttrs(allowed_attr_name_list, **kwargs)

        def createAttr(attr_name: str, **kwargs) -> None:
            if hasattr(self, attr_name):
                # TODO: adjust error and msg
                raise ValueError("Attribute existing")

            setattr(self, attr_name, kwargs.get(attr_name, NOT_PROVIDED))

        for attr_name in allowed_attr_name_list:
            createAttr(attr_name, **kwargs)
            createAttr(self._createMetaAttrName(attr_name), **kwargs)

    # def _getMetaAttrDictForClassInstance(self, class_instance) -> dict | None:
    #     meta_attr_name = self._createMetaAttrName(class_instance.__name__)
    #     if hasattr(self, meta_attr_name):
    #         return getattr(self, meta_attr_name)
        
    #     return {}

    # ---- handle populate methods ---------------------------------------------
    def populate(self) -> Any:
        return self.__populateData(
            **self._createCustomAttrDict(self.__populateData)
        )

    def populateMany(
        self,
        min_data: int = 1,
        max_data: int = 100
    ) -> list:
        # TODO: check attributes!
        created_obj_list = []

        for _ in range(0, self.createRandomInt(min_data, max_data)):
            created_obj_list.append(self.populate())

        return created_obj_list

    @classmethod
    def populateWithData(
        cls,
        obj_to_populate,
        data_list: list[dict]
    ) -> list:
        # TODO: check attributes!
        created_obj_list = []

        for data in data_list:
            created_obj_list.append(cls(obj_to_populate, **data).populate())

        return created_obj_list


################################################################################
##### class to populate fields #################################################
################################################################################

class PopulateField(BasePopulate):
    SUPPORTED_TYPE_LIST = [
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

    def __init__(
        self,
        field: models.Field,
        meta__custom_populate: Any | Callable = NOT_PROVIDED,
        meta__chance_for_default: float = 0.25,
        **kwargs
    ) -> None:
        self._checkPercentageDefinition(
            meta__chance_for_default,
            "meta__chance_for_default"
        )

        self.__field                = field
        self.__custom_populate      = meta__custom_populate
        self.__chance_for_default   = meta__chance_for_default

        super().__init__(self.__field.__class__, **kwargs)

    @property
    def field(self) -> models.Field:
        return self.__field

    @property
    def custom_populate(self) -> Any | Callable:
        return self.__custom_populate

    @property
    def chance_for_default(self) -> float:
        return self.__chance_for_default

    @classmethod
    def createRandomDict(
        cls,
        min_elements: int = 1,
        max_elements: int = 10,
    ) -> dict:
        random_data_dict = {}

        for i in range(cls.createRandomInt(min_elements, max_elements)):
            type_to_populate = cls.randomChoice(super().SUPPORTED_TYPE_LIST)
            random_data_dict[f'key_{i}'] = BasePopulate(
                type_to_populate
            ).populate()

        return random_data_dict

    # ---- Handle data population ----------------------------------------------
    def populate(self) -> Any:
        # TODO: Check if default=null and null=False is possible at model!

        # NOTE: chance_for_default must be set manually to 0.0 if the default
        # is not wanted!
        if self.field.default != NOT_PROVIDED\
        and self.randomTrue(self.chance_for_default):
            return self.field.default

        # TODO: check type of populated value correspond to field type?
        if self.custom_populate != NOT_PROVIDED:
            if isinstance(self.custom_populate, Callable):
                populated_value = self.custom_populate()
            else:
                populated_value = self.custom_populate
        else:
            populated_value = super().populate()

        if not self.field.null and populated_value is None:
            raise ValueError(f'''
                The field with the name "{self.field.name}" is not allowed to
                be null! Apparently the configurations of the model and the 
                Populate methods contradict each other.
            ''')

        return populated_value

    # ---- Handle validator logic ----------------------------------------------
    @staticmethod
    def raiseErrorIfValidatorListIsIncompatibleForField(
        field: Any,
        allowed_validator_list: list
    ):
        if not all(
            type(validator) in allowed_validator_list
            for validator in field.validators
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

        return self.createRandomInt(
            **{
                "min_value": negative_border_value,
                "max_value": positive_border_value,
                **self.__getMinMaxValidatorsInfoDict({
                    MinValueValidator: "min_value",
                    MaxValueValidator: "max_value"
                })
            }
        )

    def createRandomIntegerField(self) -> int:
        return self.__populateIntegerFields(2147483647)

    def createRandomPositiveIntegerField(self) -> int:
        return self.__populateIntegerFields(2147483647, True)

    def createRandomSmallIntegerField(self) -> int:
        return self.__populateIntegerFields(32767)

    def createRandomPositiveSmallIntegerField(self) -> int:
        return self.__populateIntegerFields(32767, True)

    def createRandomBigIntegerField(self) -> int:
        return self.__populateIntegerFields(9223372036854775807)

    def createRandomBigSmallIntegerField(self) -> int:
        return self.__populateIntegerFields(9223372036854775807, True)

    # ---- Handle float field methods ------------------------------------------
    def createRandomFloatField(self) -> float:
        self.raiseErrorIfValidatorListIsIncompatibleForField(self.field, [])

        return self.createRandomFloat()

    # ---- Handle decimal field methods ----------------------------------------
    def createRandomDecimalField(self) -> Decimal:
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

    def createRandomDateTimeField(self) -> datetime | None:
        return self.__populateDateTimeFields(self.createRandomDatetime())

    def createRandomDateField(self) -> date | None:
        return self.__populateDateTimeFields(self.createRandomDate())

    def createRandomTimeField(self) -> time | None:
        return self.__populateDateTimeFields(self.createRandomTime())

    # ---- Handle text field methods -------------------------------------------
    def __populateTextFields(self) -> str:
        return self.createRandomStr(
            **{
                "min_length": 0,
                "max_length": 1000,
                **self.__getMinMaxValidatorsInfoDict({
                    MinLengthValidator: "min_length",
                    MaxLengthValidator: "max_length"
                })
            }
        )

    def createRandomCharField(self) -> str:
        return self.__populateTextFields()

    def createRandomTextField(self) -> str:
        return self.__populateTextFields()

    # ---- Handle email field methods ------------------------------------------
    def createRandomEmailField(self) -> str:
        self.raiseErrorIfValidatorListIsIncompatibleForField(self.field, [])
        if self.field.max_length != 254:
            raise NotImplementedYet(f'''
                The field type EmailField with a max_length other than 254 is 
                not yet supported! Try setting the max_length to 254 or adjust 
                the _populateEmailField function.
            ''')

        return self.createRandomEmail()

    # ---- Handle boolean field methods ----------------------------------------
    def createRandomBooleanField(self) -> bool | None:
        self.raiseErrorIfValidatorListIsIncompatibleForField(self.field, [])

        return self.createRandomBool(can_be_none=self.field.null)

    # ---- Handle json field methods -------------------------------------------
    def createRandomJSONField(self) -> str:
        self.raiseErrorIfValidatorListIsIncompatibleForField(self.field, [])

        return self.createRandomJSON()

    # ---- Handle relationship field methods -----------------------------------
    def __populateRelationshipFields(
        self,
        relationship_model_list: list[models.Model]
    ) -> models.Model:
        if len(relationship_model_list) != 0 and self.randomTrue(0.75):
            return self.randomChoice(relationship_model_list)

        return PopulateModel(self.field.related_model).populate()

    def createRandomForeignKey(self) -> models.Model:
        self.raiseErrorIfValidatorListIsIncompatibleForField(self.field, [])

        if self.field.unique:
            return self._createRandomOneToOneField()

        return self.__populateRelationshipFields(
            self.field.related_model.objects.all()
        )

    def createRandomOneToOneField(self) -> models.Model:
        # self.raiseErrorIfValidatorListIsIncompatibleForField(self.field, [])

        # -> return self.__populateRelationshipFields(
        #       self.field.related_model.objects.filter(f"{model_name}__isnull"=True)
        # )

        raise NotImplementedYet(f"""
            OneToOneFields (or ForeignKey with unique=True) are currently not 
            supported. As soon as there is a field that meets these conditions, 
            this method must be implemented.
        """)

    def createRandomManyToManyField(
        self,
        min_relations: int = 1,
        max_relations: int = 10
    ) -> list[models.Model]:
        self.raiseErrorIfValidatorListIsIncompatibleForField(self.field, [])

        many_to_many_list = []
        related_model_list = self.field.related_model.objects.all()
        used_model_id_list = []

        for _ in range(
            self.createRandomInt(min_relations, max_relations)
        ):
            random_model = self.__populateRelationshipFields([
                related_model for related_model in related_model_list
                if related_model.id not in used_model_id_list
            ])
            many_to_many_list.append(random_model)

            if random_model in related_model_list:
                used_model_id_list.append(random_model.id)

        return many_to_many_list


################################################################################
##### class to populate models #################################################
################################################################################

class PopulateModel(BasePopulate):
    def __init__(
        self,
        model: models.Model,
        meta__chance_for_default: float = 0.25,
        meta__max_data_creation_attempts: int = 25,
        **kwargs
    ) -> None:
        self._checkType(
            model,
            models.base.ModelBase,
            "model"
        )
        self._checkType(
            meta__max_data_creation_attempts,
            int,
            "meta__max_data_creation_attempts"
        )

        self.__model                        = model
        self.__chance_for_default           = meta__chance_for_default
        self.__max_data_creation_attempts   = meta__max_data_creation_attempts

        # NOTE: The meta attribute for the primary key field has no effect
        self._createCustomAndMetaAttrs(self.__getFieldNameList(), **kwargs)

    @property
    def model(self) -> models.Model:
        return self.__model

    @property
    def chance_for_default(self) -> float:
        return self.__chance_for_default

    @property
    def max_data_creation_attempts(self) -> int:
        return self.__max_data_creation_attempts

    def _getAttr(self, attr_name: str) -> Any:
        if not hasattr(self, attr_name):
            # TODO: adjust error and msg
            raise ValueError("Attribute existing")
        
        return getattr(self, attr_name)

    def __getCustomPopulateForFieldName(self, field_name:str) -> Any:
        custom_populate = self._getAttr(field_name)

        if custom_populate == NOT_PROVIDED:
            return\
                BaseCustomValidator.getValidatorFromValidatorListWithFieldName(
                    field_name,
                    self.model.validator_list
                )

        return custom_populate

    def __createFieldDefinitionDict(self, field_name:str) -> Dict[str, Any]:
        custom_populate = self.__getCustomPopulateForFieldName(field_name)
        custom_definition_dict = self._getAttr(
            self._createMetaAttrName(field_name)
        )

        field_definition_dict = {
            "meta__chance_for_default": self.chance_for_default,
        }
        if custom_definition_dict != NOT_PROVIDED:
            field_definition_dict = {
                **field_definition_dict,
                **custom_definition_dict
            }
        if custom_populate != NOT_PROVIDED:
            field_definition_dict["meta__custom_populate"] = custom_populate

        return field_definition_dict

    def __populateDataForField(self, field) -> Any:
        field_definition_dict = self.__createFieldDefinitionDict(field.name)

        return PopulateField(field, **field_definition_dict).populate()

    def __populateModelWithFieldNameList(
        self,
        field_name_list: list[str]
    ) -> None:
        for field_name in field_name_list:
            field = self.model._meta.get_field(field_name)

            if type(field) in [ManyToOneRel, ManyToManyRel, OneToOneRel]:
                continue
            
            field_data = None
            if field.primary_key:
                primary_key_data = self._getAttr(field.name)
                if primary_key_data != NOT_PROVIDED:
                    field_data = primary_key_data
            else:
                field_data = self.__populateDataForField(
                    self.model._meta.get_field(field_name)
                )

            if type(field) == ManyToManyField:
                if self.relationship_dict == NOT_CONFIGURED:
                    self.relationship_dict = {field.name: field_data}
                else:
                    self.relationship_dict[field.name] = field_data
            else:
                setattr(self.model_obj, field_name, field_data)

    def __getFieldNameList(self) -> list[str]:
        return [
            field.name for field in self.model._meta.get_fields()
            if type(field) not in [ManyToOneRel, ManyToManyRel, OneToOneRel]
        ]

    def __checkValidationForModel(self):
        try:
            self.model_obj.full_clean()
            return []
        except ValidationError as e:
            error_field_name_list = []
            for key, value in e.error_dict.items():
                if len(value) == 1\
                and value[0].message == 'This field cannot be blank.':
                    continue

                if key == '__all__':
                    for constraint in self.model._meta.constraints:
                        if isinstance(constraint, models.UniqueConstraint):
                            error_field_name_list += constraint.fields
                        else:
                            # TODO: adjust error msg
                            raise TypeError("Constraint is not supported yet!")
                else:
                    error_field_name_list.append(key)

            return error_field_name_list
        except Exception as e:
            raise e

    def __populateModel(self) -> None:
        error_field_name_list = []

        for _ in range(0, self.max_data_creation_attempts):
            if error_field_name_list:
                self.__populateModelWithFieldNameList(error_field_name_list)
            else:
                self.__populateModelWithFieldNameList(
                    self.__getFieldNameList()
                )

            error_field_name_list = self.__checkValidationForModel()

            if not error_field_name_list:
                return

        raise ValueError(f'''
            No data can be created for the {self.model}
            Check model and populate definitions are correct!
        ''')

    @createTempAttrs("model_obj", "relationship_dict")
    def populate(self):
        self.model_obj = self.model()
        self.__populateModel()
        self.model_obj.save()

        if self.relationship_dict != NOT_CONFIGURED:
            # TODO: Can there be validation errors for many to many rel?
            for field_name, rel_model_list in self.relationship_dict.items():
                field_attr = getattr(self.model_obj, field_name)
                field_attr.set(rel_model_list)

            self.model_obj.save()

        return self.model_obj


################################################################################
##### class to populate managers ###############################################
################################################################################

class PopulateManager(BasePopulate):
    def __init__(
        self,
        manager: GeneralManager,
        meta__chance_for_default: float = 0.25,
        meta__max_data_creation_attempts: int = 25,
        meta__max_history_points: int = 3,
        meta__chance_for_deactivation: float = 0.5,
        meta__max_data_extension_points:int = 10,
        **kwargs
    ) -> None:
        # self._checkType(
        #     manager,
        #     GeneralManager,
        #     "manager"
        # )
        self._checkType(
            meta__max_history_points,
            int,
            "meta__max_history_points"
        )
        self._checkPercentageDefinition(
            meta__chance_for_deactivation,
            "meta__chance_for_deactivation"
        )
        self._checkType(
            meta__max_data_extension_points,
            int,
            "meta__max_data_extension_points"
        )

        self.__manager = manager

        self.__chance_for_default         = meta__chance_for_default
        self.__max_data_creation_attempts = meta__max_data_creation_attempts
        self.__max_history_points         = meta__max_history_points
        self.__chance_for_deactivation    = meta__chance_for_deactivation
        # NOTE: If it is necessary to specifically control the maximum data 
        # extension entries per table, an implementation must be found for this.
        self.__max_data_extension_points  = meta__max_data_extension_points

        self._createCustomAndMetaAttrs(
            [
                self._createMetaAttrName(model_obj.__name__) for model_obj in
                [
                    self.manager.group_model,
                    self.manager.data_model,
                    *self.manager.data_extension_model_list
                ]
            ],
            **kwargs
        )

    @property
    def manager(self) -> GeneralManager:
        return self.__manager

    @property
    def chance_for_default(self) -> float:
        return self.__chance_for_default

    @property
    def max_data_creation_attempts(self) -> int:
        return self.__max_data_creation_attempts

    @property
    def max_history_points(self) -> int:
        return self.__max_history_points

    @property
    def chance_for_deactivation(self) -> float:
        return self.__chance_for_deactivation

    @property
    def max_data_extension_points(self) -> int:
        return self.__max_data_extension_points

    def _populateModelDataWithMetaAttribute(
        self,
        model: models.Model,
        custom_kwargs: dict = {}
    ) -> models.Model:
        return PopulateModel(
            model,
            **{
                "meta__chance_for_default": self.chance_for_default,
                "meta__max_data_creation_attempts":
                    self.max_data_creation_attempts,
                **self._createCustomAttrDict(model),
                **custom_kwargs
            }
        ).populate()
    
    @staticmethod
    def _createCustomKwargsWithForeignKeyRelation(
        rel_model: models.Model,
        rel_model_obj: models.Model
    ) -> Dict[str, models.Model]:
        return {
            f"{transferToSnakeCase(rel_model.__name__)}": rel_model_obj
        }

    def populate(self) -> None:
        group_obj = self._populateModelDataWithMetaAttribute(
            self.manager.group_model
        )
        random_history_point_count = self.createRandomInt(
            1,
            self.max_history_points
        )

        for i in range(1, random_history_point_count+1):
            model_kwargs = self._createCustomKwargsWithForeignKeyRelation(
                self.manager.group_model,
                group_obj
            )
            # TODO: Rework logic for deactivation
            if i == random_history_point_count and i != 1\
            and self.randomTrue(self.chance_for_deactivation):
                model_kwargs["active"] = False
            else:
                model_kwargs["active"] = True

            data_obj = self._populateModelDataWithMetaAttribute(
                self.manager.data_model,
                model_kwargs
            )

            data_extension_kwargs =\
                self._createCustomKwargsWithForeignKeyRelation(
                    self.manager.data_model,
                    data_obj
                )

            for data_extension_model in self.manager.data_extension_model_list:
                random_data_extension_count = self.createRandomInt(
                    1,
                    self.max_data_extension_points
                )
                for _ in range(1, random_data_extension_count):
                    self._populateModelDataWithMetaAttribute(
                        data_extension_model,
                        data_extension_kwargs
                    )

        return self.manager(group_obj.id)