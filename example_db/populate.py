from django.db.models.fields.reverse_related import ManyToOneRel
from django.db.models.fields import NOT_PROVIDED
from django.db.models import Model
from backend.models import GroupTable, DataTable, DataExtensionTable, User
from backend.src.auxiliary.manager import transferToSnakeCase
from datetime import datetime, timedelta
from faker import Faker
import random

class GeneralPopulate:
    max_history_points: int = 3
    chance_for_no_change: float = 0.7
    chance_for_deactivation: float = 0.5

    group_definition: tuple[GroupTable, ] = ()
    data_definition: tuple[DataTable, callable] = ()
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
        if not isinstance(self.max_history_points, int):
            raise ValueError(f'''
                Definition for "max history points" is not an integer!
            ''')
        
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
        self.group_data_dict = self.__createDataWithDefinitionTuple(self.group_definition)

        for _ in range(random.randint(1, self.max_history_points)):
            self.data_data_list.append(
                self.__createDataWithDefinitionTuple(self.data_definition)
            )

            for data_extension_definition in self.data_extension_definition_list:
                self.data_extension_list.append(
                    self.__createDataWithDefinitionTuple(data_extension_definition)
                )

        self.__deactivateLastObjectRandomly()

    # ---- Handle group model data ---------------------------------------------
    def __createAndSaveGroupObject(self) -> GroupTable:
        group_data_dict = self.__checkForPredeterminedData(self.group_data_dict)
        group_model, _ = self.group_definition

        return self.__createAndSaveModelObject(
            group_model,
            group_data_dict
        )

    # ---- Handle data model data ----------------------------------------------
    def __deactivateLastObjectRandomly(self):
        if self.randomChoice(self.chance_for_deactivation):
            previous_data_dict = self.__getLatestDataDict()

            if not len(previous_data_dict):
                raise ValueError("No data object to deactivate!")

            base_data_dict = self.__createBaseDataDict(previous_data_dict)

            self.data_data_list.append(
                {**previous_data_dict, **base_data_dict, 'active': 0}
            )
    
    def __createAndSaveDataObject(
        self,
        data_data_dict: dict,
        group_object: GroupTable
    ) -> DataTable:
        data_data_dict = self.__checkForPredeterminedData(data_data_dict)
        group_object, _ = self.group_definition
        data_object, _ = self.data_definition

        return self.__createAndSaveModelObject(
            data_object,
            {
                **{self.getColumnNameForModel(group_object): group_object},
                **data_data_dict
            }
        )

    # ---- Handle data extension model data ------------------------------------    
    def __createAndSaveDataExtensionObject(
        self,
        data_extension_model_obj: Model,
        data_extension_dict: dict,
        data_object: DataTable
    ) -> Model:
        data_object, _ = self.data_definition

        return self.__createAndSaveModelObject(
            data_extension_model_obj,
            {
                **{self.getColumnNameForModel(data_object): data_object},
                **data_extension_dict
            }
        )

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
        model_object = model_obj(**data_dict)
        model_object.save()
        return model_object
    
    def save(self):
        group_object = self.__createAndSaveGroupObject()

        for data_data_dict in self.data_data_list:
            data_object = self.__createAndSaveDataObject(
                data_data_dict,
                group_object
            )

            for data_extension_index, data_extension_list_of_dict in enumerate(
                self.data_extension_list
            ):
                for data_extension_dict in data_extension_list_of_dict:
                    data_extension_object, _ =\
                        self.data_extension_definition_list[
                            data_extension_index
                        ]
                    
                    self.__createAndSaveDataExtensionObject(
                        data_extension_object,
                        data_extension_dict,
                        data_object
                    )

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

        return self.__createDataDataDict(data_dict)\
            if model_obj.table_type == "DataTable" else data_dict

    # ---- Handle data configuration check -------------------------------------
    @staticmethod
    def getDirectColumnNameList(model_obj: Model) -> list[str]:
        return [
            field.name for field in model_obj._meta.get_fields()
            if type(field) != ManyToOneRel
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
    def getIncorectlyConfiguredColumnNameList(
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
            self.getIncorectlyConfiguredColumnNameList(
                [*column_name_list, *column_name_list_to_disregard],
                data_dict
            )

        has_unconfigured_columns = len(unconfigured_columns)
        has_incorrectly_configured_columns = len(incorrectly_configured_columns)

        error_msg = ""
        if has_unconfigured_columns:
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
    
    def __createDataDataDict(self, data_dict: dict) -> dict:
        data_data_dict = {
            field_name: self.__decideBetweenPreviousOrNewData(
                field_name,
                data_value
            ) for field_name, data_value in data_dict.items()
        }
        base_data_dict = self.__createBaseDataDict(data_data_dict)

        return {**base_data_dict, **data_data_dict}

    # ---- Check and select previous data data ---------------------------------
    @staticmethod
    def getDefaultValueFields(model: Model) -> list:
        return [
            field.name for field in model._meta.get_fields()
            if field.default != NOT_PROVIDED and type(field) != ManyToOneRel
        ]

    def __createDataDataDictWithDefaultValues(self, data_dict: dict) -> dict:
        # TODO: Check if this really works!
        model_obj, _ = self.data_definition
        default_field_list = self.getDefaultValueFields(model_obj)

        return {
            field_name: data_value 
            for field_name, data_value in data_dict.items()
            if field_name not in default_field_list or 
            (field_name in default_field_list and 
                self.randomChoice(self.chance_for_no_change))
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
        if len(self.data_data_list) == 0:
            return self.__createDataDataDictWithDefaultValues(data_value)

        latest_data = self.__getLatestData(field_name)

        if latest_data is not None and self.randomChoice(
            self.chance_for_no_change
        ):
            return latest_data

        return data_value

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

    @staticmethod
    def getRandomForeignKeyRelation(foreign_key_relation_obj: Model) -> object:
        foreign_key_relation_obj_list =\
            foreign_key_relation_obj.objects.order_by('?')

        if not foreign_key_relation_obj_list.exists():
            raise ValueError(
                "There are no foreign key relation objects to choose from!"
            )

        return foreign_key_relation_obj_list.first()

    @classmethod
    def getRandomInteger(
        cls,
        min_value: int = 0, 
        max_value: int = 999999
    ) -> int:
        return cls.fake.random_int(min_value, max_value)

    @classmethod
    def getRandomText(cls, max_nb_chars: int = 50) -> str:
        return cls.fake.text(max_nb_chars)

    @classmethod
    def getRandomDescription(cls) -> str:
        return cls.getRandomText(250)


    # def randomLetters(length = 4):
    #     letters = string.ascii_letters
    #     return ''.join(random.choice(letters) for _ in range(length))

    # def drawingNumberGenerator(drawing_type: str) -> str:
    #     return f'AS_{random.randint(1,99):02}_{drawing_type}_{random.randint(10000,99999):05}'

    # def getUniqueNumber(model, column_name, number_function):
    #     unique = False
    #     while not unique:
    #         number = number_function()
    #         if not model.objects.filter(**{column_name: number}):
    #             unique = True
    #     return number