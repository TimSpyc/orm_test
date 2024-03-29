from django.core.exceptions import ValidationError
from django.db.models.fields.reverse_related import ManyToOneRel, ManyToManyRel, OneToOneRel
from django.db.models.fields.related import ForeignKey, OneToOneField, ManyToManyField
from django.db.models.fields import NOT_PROVIDED
from django.db.models import Model
from backend.models import GroupTable, DataTable, DataExtensionTable, User
from backend.src.auxiliary.manager import transferToSnakeCase
from datetime import datetime, timedelta
from faker import Faker
import random
import hashlib

class GeneralPopulate:
    max_history_points: int = 3
    max_data_creation_attempts: int = 10
    chance_for_no_change: float = 0.7
    chance_for_deactivation: float = 0.5

    group_definition: tuple[GroupTable, ] = ()
    data_definition: tuple[DataTable, callable] = ()
    # TODO: All functions of the class should be checked for the right return value!
    data_extension_definition_list: list[tuple[DataExtensionTable, callable]] = []

    fake = Faker()

    def __init__(self):
        self.__checkGeneralPopulateIsProperlyConfigured()

        self.group_data_dict: dict = {}
        self.data_data_list: list[dict] = []
        self.data_extension_list: list[list[dict]] = []

        self.__populateData()

    # ---- Handle class configuration check ------------------------------------
    def __checkGeneralPopulateIsProperlyConfigured(self):    
        self.__checkIntegerDefinition(
            self.max_history_points,
            "max history points"
        )

        self.__checkIntegerDefinition(
            self.max_data_creation_attempts,
            "max data creation attempts"
        )

        self.__checkPercentageDefinition(
            self.chance_for_no_change,
            "chance for no change"
        )

        self.__checkPercentageDefinition(
            self.chance_for_deactivation,
            "chance for deactivation"
        )

        self.__checkModelDefinitionTuple(
            self.group_definition,
            "group",
            "GroupTable"
        )

        self.__checkModelDefinitionTuple(
            self.data_definition,
            "data",
            "DataTable"
        )

        # TODO: Outsourcing the check to a function!
        if not isinstance(self.data_extension_definition_list, list):
            raise ValueError(f'''
                Definition for "data extension" data is not a list!
            ''')

        for data_extension_definition_tuple in self.data_extension_definition_list:
            self.__checkModelDefinitionTuple(
                data_extension_definition_tuple,
                "data extension",
                "DataExtensionTable"
            )

    @staticmethod
    def __checkIntegerDefinition(
        integer: int,
        integer_description: str
    ):
        if not isinstance(integer, int):
            raise ValueError(f'''
                Definition for "{integer_description}" is not an integer!
            ''')

    @staticmethod
    def __checkPercentageDefinition(
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
    def __checkTupleDefinition(
        definition_tuple: tuple,
        definition_description: str
    ):
        if not isinstance(definition_tuple, tuple):
            raise ValueError(f'''
                Definition for "{definition_description}" data is not a tuple!
            ''')

        if len(definition_tuple) != 2:
            raise ValueError(f'''
                Definition tuple for "{definition_description}" data 
                has not the right length!
            ''')

    @staticmethod
    def __checkModelDefinition(
        model_obj: Model,
        definition_description: str,
        table_type: str
    ):
        if not issubclass(model_obj, Model):
            raise ValueError(f'''
                Object for "{definition_description}" table is not a model!
            ''')

        if not hasattr(model_obj, "table_type") and\
        model_obj.table_type != table_type:
            raise ValueError(f'''
                Object for "{definition_description}" table 
                is not of type "{table_type}"!
            ''')

    @staticmethod
    def __checkDataCreationFunctionDefinition(
        data_creation_function,
        definition_description: str
    ):
        if not callable(data_creation_function):
            raise ValueError(f'''
                Function for "{definition_description}" data creation 
                is not callable!
            ''')

    def __checkModelDefinitionTuple(
        self,
        definition_tuple: tuple,
        definition_description: str,
        table_type: str
    ):
        self.__checkTupleDefinition(definition_tuple, definition_description)

        model_obj, data_creation_function = definition_tuple

        self.__checkModelDefinition(
            model_obj, 
            definition_description, 
            table_type
        )

        self.__checkDataCreationFunctionDefinition(
            data_creation_function,
            definition_description
        )


    # ---- Handle data population ----------------------------------------------
    def __populateData(self):
        group_model, _ = self.group_definition
        data_model, _ = self.data_definition

        self.group_data_dict = self.__createAndCheckDataDict(
            self.group_definition
        )

        for _ in range(random.randint(1, self.max_history_points)):
            self.data_data_list.append(
                self.__createAndCheckDataDict(
                    self.data_definition,
                    self.data_data_list,
                    group_model
                )
            )

            # TODO: Check how data extension is created!
            # for data_extension_definition in self.data_extension_definition_list:
            #     self.data_extension_list.append(
            #         self.__createAndCheckDataDict(
            #             data_extension_definition,
            #             self.data_extension_list,
            #             data_model
            #         )
            #     )

        self.__deactivateLastObjectRandomly()

    # TODO: Should the function be optimized?
    def __deactivateLastObjectRandomly(self):
        if self.randomChoice(self.chance_for_deactivation):
            previous_data_dict = self.__getLatestDataDict()

            if not len(previous_data_dict):
                raise ValueError("No data object to deactivate!")

            base_data_dict = self.__createBaseDataDict(previous_data_dict)
            data_dict = {**previous_data_dict, **base_data_dict, 'active': 0}

            group_model, _ = self.group_definition
            data_model, _ = self.data_definition
            
            _, model_is_validated = self.checkDataCanBeWriteToDatabase(
                data_model,
                data_dict,
                [self.getColumnNameForModel(group_model)]
            )

            if not model_is_validated:
                raise ValueError(f'''
                    The {data_model} model can't be deactivated! 
                    Check the general conditions of your model. The function may 
                    need to be customized to deactivate it.
                ''')

            self.data_data_list.append(
                {**previous_data_dict, **base_data_dict, 'active': 0}
            )

    def __createAndCheckDataDict(
        self,
        data_extension_definition: tuple,
        data_list: list = [],
        reference_model: Model = None
    ):
        model, _ = data_extension_definition

        for _ in range(0, self.max_data_creation_attempts):
            data_dict = self.__createDataWithDefinitionTuple(
                data_extension_definition
            )

            if self.checkUniquenessAndCreateabilityOfData(
                model,
                data_dict,
                data_list,
                reference_model,
            ):
                return data_dict

        raise ValueError(f'''
            No data can be created for the {model}! 
            Check whether the model definitions are correct and the data created
            corresponds to them.
        ''')

    # ---- Handling field lists ------------------------------------------------
    @staticmethod
    def checkFieldHasRelationship(field) -> bool:
        return type(field) in [ForeignKey, OneToOneField, ManyToManyField]
    
    @staticmethod
    def getFieldListsForModel(model: Model) -> tuple[list, list]:
        data_field_list = []
        relation_field_list = []

        for field in model._meta.get_fields():
            if GeneralPopulate.checkFieldHasRelationship(field):
                relation_field_list.append(field)
            else:
                data_field_list.append(field)

        return data_field_list, relation_field_list

    # ---- Handling save process -----------------------------------------------
    def __checkForPredeterminedData(self, data_dict: dict) -> dict:
        return {
            field_name: getattr(self, field_name)\
                if hasattr(self, field_name) else data_value\
                for field_name, data_value in data_dict.items()
        }

    def __createAndSaveModelObject(
        self,
        model_obj: Model,
        data_dict: dict
    ) -> Model:
        model_object, model_is_validated = self.checkDataCanBeWriteToDatabase(
            model_obj,
            data_dict
        )

        if not model_is_validated:
            raise ValueError(f'''
                The {model_object} model can't be saved! 
                Apparently manual changes after populating the data does not 
                meet all the general conditions. Please check them all .
            ''')

        model_object.save()
        return model_object

    def __createAndSaveGroupObject(self) -> GroupTable:
        group_data_dict = self.__checkForPredeterminedData(self.group_data_dict)
        group_model, _ = self.group_definition

        return self.__createAndSaveModelObject(
            group_model,
            group_data_dict
        )

    def __createAndSaveDataObject(
        self,
        data_data_dict: dict,
        group_model_object: GroupTable
    ) -> DataTable:
        data_data_dict = self.__checkForPredeterminedData(data_data_dict)
        group_object, _ = self.group_definition
        data_object, _ = self.data_definition

        return self.__createAndSaveModelObject(
            data_object,
            {
                **{self.getColumnNameForModel(group_object): group_model_object},
                **data_data_dict
            }
        )

    def __createAndSaveDataExtensionObject(
        self,
        data_extension_model_obj: Model,
        data_extension_dict: dict,
        data_model_object: DataTable
    ) -> Model:
        data_object, _ = self.data_definition

        return self.__createAndSaveModelObject(
            data_extension_model_obj,
            {
                **{self.getColumnNameForModel(data_object): data_model_object},
                **data_extension_dict
            }
        )

    def save(self):
        group_model_object = self.__createAndSaveGroupObject()

        for data_data_dict in self.data_data_list:
            data_model_object = self.__createAndSaveDataObject(
                data_data_dict,
                group_model_object
            )

            # TODO: Sollte die extension data erst hier erstellt werden?
            for data_extension_index, data_extension_list_of_dict in enumerate(
                self.data_extension_list
            ):
                for data_extension_dict in data_extension_list_of_dict:
                    data_extension_model_object, _ =\
                        self.data_extension_definition_list[
                            data_extension_index
                        ]

                    self.__createAndSaveDataExtensionObject(
                        data_extension_model_object,
                        data_extension_dict,
                        data_model_object
                    )

        # TODO: Should data be deleted if errors occur? -> YES!

    # ---- Handle population ---------------------------------------------------
    @classmethod
    def populate(cls):
        populate_class_instance = cls()
        populate_class_instance.save()

        return populate_class_instance

    # ---- Handle data creation ------------------------------------------------
    def __createDataWithDefinitionTuple(
        self,
        definition_tuple: tuple
    ) -> dict | list[dict]:
        model_obj, dataCreationFunction = definition_tuple

        data_dict = dataCreationFunction(self)

        # TODO: Check the data_dict only once!
        self.__checkIfDataDictIsProperlyConfigured(data_dict, model_obj)

        # TODO: Are there default values in extension data? -> YES
        return self.__createDataDataDict(data_dict)\
            if model_obj.table_type == "DataTable" else data_dict

    # ---- Handle data configuration check -------------------------------------
    @staticmethod
    def checkColumnTypeCanBeIgnored(field) -> bool:
        return type(field) not in [ManyToManyRel, ManyToOneRel]
    
    @staticmethod
    def getDirectColumnNameList(model_obj: Model) -> list[str]:
        return [
            field.name for field in model_obj._meta.get_fields()
            if GeneralPopulate.checkColumnTypeCanBeIgnored(field)
        ]

    def getColumnNameListToDisregard(self, model_obj: Model) -> list:
        group_obj, _ = self.group_definition
        data_model_name = self.getColumnNameForModel(group_obj)

        column_name_list_to_disregard = ["id"]
        if model_obj.table_type == "GroupTable":
            column_name_list_to_disregard += self.getDirectColumnNameList(
                GroupTable
            )
        elif model_obj.table_type == "DataTable":
            column_name_list_to_disregard += self.getDirectColumnNameList(
                DataTable
            )
            column_name_list_to_disregard.append(data_model_name)
        elif model_obj.table_type == "DataExtensionTable":
            column_name_list_to_disregard += self.getDirectColumnNameList(
                DataExtensionTable
            )
            column_name_list_to_disregard.append(data_model_name[:-6])

        return column_name_list_to_disregard

    def getReducedColumnNameList(
        self,
        model_obj: Model,
        column_name_list_to_disregard: list
    ) -> list:
        column_name_list = self.getDirectColumnNameList(model_obj)

        return [
            column_name for column_name in column_name_list
            if column_name not in column_name_list_to_disregard
        ]

    @staticmethod
    def getUnconfiguredColumnNameList(
        column_name_list: list,
        data_dict: dict
    ) -> list:
        return [
            unconfigured_column_name
            for unconfigured_column_name in column_name_list
            if unconfigured_column_name not in data_dict.keys()
        ]

    @staticmethod
    def getIncorrectlyConfiguredColumnNameList(
        column_name_list: list,
        data_dict: dict
    ) -> list:
        return [
            incorrectly_configured_column_name
            for incorrectly_configured_column_name in data_dict.keys()
            if incorrectly_configured_column_name not in column_name_list
        ]

    def __checkIfDataDictIsProperlyConfigured(
        self,
        data_dict: dict,
        model_obj: Model
    ):
        column_name_list_to_disregard = self.getColumnNameListToDisregard(
            model_obj
        )
        column_name_list = self.getReducedColumnNameList(
            model_obj,
            column_name_list_to_disregard
        )

        unconfigured_columns = self.getUnconfiguredColumnNameList(
            column_name_list,
            data_dict
        )

        incorrectly_configured_columns =\
            self.getIncorrectlyConfiguredColumnNameList(
                [*column_name_list, *column_name_list_to_disregard],
                data_dict
            )

        has_unconfigured_columns = len(unconfigured_columns)
        has_incorrectly_configured_columns = len(incorrectly_configured_columns)

        error_msg = ""
        if has_unconfigured_columns:
            # TODO: Adjust error message! -> Which model?
            error_msg += f"""
                The following columns appear in the model 
                but are not configured: {unconfigured_columns}
            """
        if has_incorrectly_configured_columns:
            error_msg += f"""
                The following columns are configured 
                but do not appear in the model: {incorrectly_configured_columns}
            """

        if has_unconfigured_columns or has_incorrectly_configured_columns:
            raise ValueError(error_msg)

    # ---- Handle additional data logic for data model -------------------------
    def __createBaseDataDict(self, data_data_dict: dict) -> dict:
        reference_date = self.__getReferenceDate(data_data_dict)

        return {
            'creator': self.__decideBetweenPreviousOrNewData(
                'creator',
                self.getRandomForeignKeyRelation(User)
            ),
            'date': self.getRandomDateTime(reference_date),
            'active': 1
        }
    
    def __createDataDataDict(self, data_dict: dict,) -> dict:
        # TODO: Check selection of default values!
        if len(self.data_data_list) == 0:
            data_data_dict = self.__createDataDataDictWithDefaultValues(data_dict)
        else: 
            data_data_dict = {
                field_name: self.__decideBetweenPreviousOrNewData(
                    field_name,
                    data_value
                ) for field_name, data_value in data_dict.items()
            }

        base_data_dict = self.__createBaseDataDict(data_data_dict)

        return {**base_data_dict, **data_data_dict}

    # ---- Check unique columns ------------------------------------------------
    @staticmethod
    def getUniqueTogetherList(model: Model) -> list:
        return model._meta.unique_together

    @staticmethod
    def getNameListForUniqueColumns(model: Model) -> list:
        return [
            field.name for field in model._meta.get_fields()
            if GeneralPopulate.checkColumnTypeCanBeIgnored(field)
            and field.unique
        ]

    @staticmethod
    def checkUniquenessAndCreateabilityOfData(
        model: Model,
        data_dict: dict,
        data_list: list = [],
        reference_model: Model = None,
    ) -> bool:
        data_unique_in_data_list = True if not len(data_list) else\
            GeneralPopulate.checkUniquenessOfDataForModelInDataList(
                model,
                data_dict,
                data_list
            )

        column_list_to_ignore = [GeneralPopulate.getColumnNameForModel(
            reference_model
        )] if reference_model is not None else []

        _, data_unique_in_data_base =\
            GeneralPopulate.checkDataCanBeWriteToDatabase(
                model,
                data_dict,
                column_list_to_ignore
            )

        return data_unique_in_data_list and data_unique_in_data_base

    @staticmethod
    def checkDataCanBeWriteToDatabase(
        model: Model,
        data_dict: dict,
        column_name_list_to_ignore: list = []
    ) -> bool:
        initialized_model = model(**data_dict)

        model_is_validated = GeneralPopulate.validateWholeModel(
            initialized_model,
            column_name_list_to_ignore
        )

        return initialized_model, model_is_validated

    @staticmethod
    def checkUniquenessOfDataForModelInDataList(
        model: Model,
        data_dict: dict,
        data_list: list
    ) -> bool:
        columns_are_unique = GeneralPopulate.checkColumnsAreUnique(
            model,
            data_dict,
            data_list
        )
        columns_are_unique_together =\
            GeneralPopulate.checkColumnsAreUniqueTogether(
                model,
                data_dict,
                data_list
            )

        return columns_are_unique and columns_are_unique_together

    @staticmethod
    def checkColumnsAreUnique(
        model: Model,
        data_dict: dict,
        data_list: list
    ) -> bool:
        column_list_to_ignore =\
            GeneralPopulate.getColumnNameListWithDefaultValue(
                model,
                data_dict
            )
        unique_column_name_list = GeneralPopulate.getNameListForUniqueColumns(
            model
        )

        testUniqueConditionIsViolated =\
            lambda existing_data_dict, new_data_dict: any(
                GeneralPopulate.createListOfUniquenessViolatingState(
                    existing_data_dict,
                    new_data_dict,
                    unique_column_name_list,
                    [*column_list_to_ignore, "id"]
                )
            )

        if GeneralPopulate.checkUniqueConditionIsViolated(
            data_list,
            data_dict,
            testUniqueConditionIsViolated
        ): return False

        return True

    @staticmethod
    def checkColumnsAreUniqueTogether(
        model: Model,
        data_dict: dict,
        data_list: list
    ) -> bool:
        column_list_to_ignore =\
            GeneralPopulate.getColumnNameListWithDefaultValue(
                model,
                data_dict
            )
        unique_together_list_of_list = GeneralPopulate.getUniqueTogetherList(
            model
        )

        for unique_together_list in unique_together_list_of_list:
            testUniqueConditionIsViolated =\
                lambda existing_data_dict, new_data_dict: all(
                    GeneralPopulate.createListOfUniquenessViolatingState(
                        existing_data_dict,
                        new_data_dict,
                        unique_together_list,
                        column_list_to_ignore
                    )
                )

            if GeneralPopulate.checkUniqueConditionIsViolated(
                data_list,
                data_dict,
                testUniqueConditionIsViolated
            ): return False

        return True

    @staticmethod
    def checkUniqueConditionIsViolated(
        existing_data_list: list,
        new_data_dict: dict,
        testUniqueConditionIsViolated: callable,
    ):
        matching_data_list = [
            existing_data_dict for existing_data_dict in existing_data_list
            if testUniqueConditionIsViolated(existing_data_dict, new_data_dict)
        ]

        return len(matching_data_list) > 0

    @staticmethod
    def createListOfUniquenessViolatingState(
        existing_data_dict: dict,
        new_data_dict: dict,
        unique_column_name_list: list,
        column_name_list_to_ignore: list = []
    ) -> bool:
        return [
            existing_data_dict.get(column_name) == new_data_dict.get(column_name)
            for column_name in unique_column_name_list
            if column_name not in column_name_list_to_ignore
        ]

    # TODO: Rename function to getColumnNamesWithDefaultValueForDataDict?
    @staticmethod
    def getColumnNameListWithDefaultValue(
        model: Model,
        data_dict: dict
    ) -> list:
        return [
            field.name for field in model._meta.get_fields()
            if GeneralPopulate.checkColumnTypeCanBeIgnored(field)
            and field.default == data_dict.get(field.name)
        ]

    # ---- Validation checks for model -----------------------------------------
    @staticmethod
    def validateFieldsForModel(
        initialized_model: Model,
        column_name_list_to_ignore: list = []
    ) -> bool:
        return GeneralPopulate.checkValidationForModel(
            lambda: initialized_model.clean_fields(
                exclude=column_name_list_to_ignore
            )
        )

    @staticmethod
    def validateFieldUniquenessForModel(
        initialized_model: Model,
        column_name_list_to_ignore: list = []
    ) -> bool:
        return GeneralPopulate.checkValidationForModel(
            lambda: initialized_model.validate_unique(
                exclude=column_name_list_to_ignore
            )
        )

    @staticmethod
    def validateConstraintsForModel(
        initialized_model: Model,
        column_name_list_to_ignore: list = []
    ) -> bool:
        return GeneralPopulate.checkValidationForModel(
            lambda: initialized_model.validate_constraints(
                exclude=column_name_list_to_ignore
            )
        )

    @staticmethod
    def validateCustomConstraintsForModel(
        initialized_model: Model,
        column_name_list_to_ignore: list = []
    ) -> bool:
        return GeneralPopulate.checkValidationForModel(
            lambda: initialized_model.clean(
                exclude=column_name_list_to_ignore
            )
        )

    @staticmethod
    def validateWholeModel(
        initialized_model: Model,
        column_name_list_to_ignore: list = []
    ) -> bool:
        return GeneralPopulate.checkValidationForModel(
            lambda: initialized_model.full_clean(
                exclude=column_name_list_to_ignore
            )
        )

    @staticmethod
    def checkValidationForModel(
        validationModelCheck: callable
    ) -> bool:
        try:
            validationModelCheck()
        except ValidationError as e:
            return GeneralPopulate._dismissBlankFieldErrors(e)
        else:
            return True

    @staticmethod
    def _dismissBlankFieldErrors(validation_error: ValidationError) -> bool:
        for error_desc_list in validation_error.error_dict.values():
            if len(error_desc_list) > 1 or\
            error_desc_list[0].message != 'This field cannot be blank.':
                return False

        return True

    # ---- Check and select previous data data ---------------------------------
    @staticmethod
    def getDefaultValueColumnDict(model: Model) -> list:
        return {
            field.name: field.default for field in model._meta.get_fields()
            if GeneralPopulate.checkColumnTypeCanBeIgnored(field)
            and field.default != NOT_PROVIDED
        }

    def __createDataDataDictWithDefaultValues(self, data_dict: dict) -> dict:
        data_model, _ = self.data_definition
        default_column_dict = self.getDefaultValueColumnDict(data_model)

        return {
            **default_column_dict,
            **{
                field_name: data_value 
                for field_name, data_value in data_dict.items()
                if field_name not in default_column_dict.keys() or 
                (field_name in default_column_dict.keys() and 
                    self.randomChoice(self.chance_for_no_change))
            }
        }
    
    def __getLatestDataDict(self) -> DataTable:
        if isinstance(self.data_data_list, list)\
        and len(self.data_data_list):
            return self.data_data_list[-1]

        return None

    def __getLatestData(self, field_name: str) -> any:
        latest_data_dict = self.__getLatestDataDict()

        if latest_data_dict is not None:
            if field_name not in latest_data_dict.keys():
                raise ValueError(f'''
                    Key "{field_name}" not in "latest_data_dict"!
                ''')

            return latest_data_dict[field_name]

        return None

    def __decideBetweenPreviousOrNewData(
        self,
        field_name: str,
        data_value: any
    ) -> any:
        latest_data = self.__getLatestData(field_name)

        if latest_data is not None and self.randomChoice(
            self.chance_for_no_change
        ):
            return latest_data

        return data_value

    # ---- Handle model relationships ------------------------------------------
    def getModelRelation(self, field_name: str) -> Model | list[Model]:
        pass

    @staticmethod
    def getRandomForeignKeyRelation(foreign_key_relation_obj: Model) -> object:
        foreign_key_relation_obj_list =\
            foreign_key_relation_obj.objects.order_by('?')

        if not foreign_key_relation_obj_list.exists():
            raise ValueError(
                "There are no foreign key relation objects to choose from!"
            )

        return foreign_key_relation_obj_list.first()

    @staticmethod
    def getRandomManyToManyFieldList(
        many_to_many_obj: Model,
        min_value: int = 1,
        max_value: int = 1
    ) -> list[Model]:
        related_objects = random.sample(
            list(many_to_many_obj.objects.all()), 
            GeneralPopulate.getRandomInteger(min_value, max_value)
        )

        return related_objects

    # ---- Handle datetime logic -----------------------------------------------
    def __getReferenceDate(self, data_data_dict: dict) -> datetime:
        latest_data_dict = self.__getLatestDataDict()

        if latest_data_dict is not None:
            reference_date = latest_data_dict["date"]
        else:
            reference_date = None

        for data_data in data_data_dict.values():
            is_group_table_model = isinstance(data_data, Model)\
                and getattr(data_data, "table_type") == "GroupTable"

            if is_group_table_model and (reference_date is None\
            or data_data.date > reference_date):
                # TODO: Check if this really works!
                data_object, _ = self.data_definition
                data_model = data_object.objects.filter(group_id=data_data.id).latest()
                reference_date = data_model.date

        return reference_date

    @staticmethod
    def createDatetimeStartAndEnd(reference_date: datetime) -> tuple:
        if reference_date is None:
            datetime_end = datetime.now()
            datetime_start = datetime_end - timedelta(days=2*365)
        else:
            datetime_start = reference_date
            datetime_end = datetime_start + timedelta(days=7)

        return datetime_start, datetime_end

    @staticmethod
    def fakeDateBetweenDates(
        datetime_start: datetime,
        datetime_end: datetime
    ) -> datetime:
        fake = Faker()
        return fake.date_time_between_dates(
            datetime_start=datetime_start,
            datetime_end=datetime_end
        )

    @staticmethod
    def checkIfDateIsWorkday(date: datetime) -> bool:
        return date.weekday() < 5

    @staticmethod
    def getRandomDateTime(
        reference_date: datetime = None
    ) -> datetime:
        datetime_start, datetime_end =\
            GeneralPopulate.createDatetimeStartAndEnd(reference_date)

        random_date = GeneralPopulate.fakeDateBetweenDates(
            datetime_start,
            datetime_end
        )

        while not GeneralPopulate.checkIfDateIsWorkday(random_date):
            random_date = GeneralPopulate.fakeDateBetweenDates(
                datetime_start,
                datetime_end
            )

        return random_date

    # ---- Handle static methods -----------------------------------------------
    @staticmethod
    def getColumnNameForModel(model: Model) -> str:
        return transferToSnakeCase(model.__name__)
    
    @staticmethod
    def getColumnNameForModelObject(model_object: object) -> str:
        return transferToSnakeCase(model_object.__class__.__name__)

    @staticmethod
    def randomChoice(chance_for_false):
        random_choice = random.randint(1, 100)/100
        return random_choice > chance_for_false

    # TODO: get the foreign_key_relation_obj from the model_obj or column name?
    @staticmethod
    def getRandomForeignKeyRelation(foreign_key_relation_obj: Model) -> object:
        foreign_key_relation_obj_list =\
            foreign_key_relation_obj.objects.order_by('?')

        if not foreign_key_relation_obj_list.exists():
            raise ValueError(
                "There are no foreign key relation objects to choose from!"
            )

        return foreign_key_relation_obj_list.first()

    @staticmethod
    def getRandomManyToManyFieldList(
        many_to_many_obj: Model,
        min_value: int = 1,
        max_value: int = 1
    ) -> list[Model]:
        related_objects = random.sample(
            list(many_to_many_obj.objects.all()), 
            GeneralPopulate.getRandomInteger(min_value, max_value)
        )

        return related_objects

    @classmethod
    def getRandomInteger(
        cls,
        min_value: int = 0, 
        max_value: int = 999999
    ) -> int:
        return cls.fake.random_int(min_value, max_value)
    
    @staticmethod
    def getRandomFloat(
        min_value: float = 0, 
        max_value: float = 999999
    ) -> float:
        return random.uniform(min_value, max_value)

    @classmethod
    def getRandomText(cls, max_nb_chars: int = 50) -> str:
        return cls.fake.text(max_nb_chars)

    @classmethod
    def getRandomBoolean(
        cls,
        can_be_none: bool = False,
        chance_for_bool: float = 0.5
    ) -> bool | None:
        fake_boolean = cls.fake.boolean()

        if can_be_none and cls.randomChoice(chance_for_bool):
            return None

        return fake_boolean

    @classmethod
    def getRandomDescription(cls) -> str:
        return cls.getRandomText(250)
    
    @classmethod
    def getRandomHashCode(cls, random_string: str = None) -> str:
        # TODO: Use yuyu id?
        string_to_hash = random_string if random_string is not None else\
            datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

        return hashlib.md5(string_to_hash.encode()).hexdigest()