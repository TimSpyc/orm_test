# Responsible Maximilian Kelm
from datetime import datetime
from decimal import Decimal
from unittest.mock import patch
from django.test import TestCase
from django.db.models.fields import NOT_PROVIDED
from backend.models.populate import BasePopulate
from backend.src.auxiliary.exceptions import (
    IncompatibleValidatorList,
    NotImplementedYet
)

################################################################################
##### decorator to test populate classes #######################################
################################################################################

def testErrorIsNotRaised(func):
    def wrapper(self, *args, **kwargs):
        try:
            func(self, *args, **kwargs)
        except Exception as e:
            self.fail(
                f"{func.__name__} raised {type(e).__name__} unexpectedly!"
            )
    return wrapper


################################################################################
##### test base populate class #################################################
################################################################################

# ---- __init__ ----------------------------------------------------------------
class TestBasePopulateInit(TestCase):
    def test_not_supported_type(self):
        self.assertRaises(
            NotImplementedYet,
            BasePopulate,
            complex
        )

    @testErrorIsNotRaised
    def test_supported_type(self):
        BasePopulate(int)


# ---- type_to_populate --------------------------------------------------------
# NOTE: Properties that only return a self attribute are not tested!

# ---- _checkType --------------------------------------------------------------
class TestCheckType(TestCase):
    def test_incorrect_type(self):
        self.assertRaises(
            TypeError,
            BasePopulate._checkType,
            "123",
            int,
            'test_attr'
        )

    @testErrorIsNotRaised
    def test_correct_type(self):
        BasePopulate._checkType(123, int, 'test_attr')

# ---- _checkPercentageDefinition ----------------------------------------------
class TestCheckPercentageDefinition(TestCase):
    def test_incorrect_percentage(self):
        self.assertRaises(
            ValueError,
            BasePopulate._checkPercentageDefinition,
            1.5,
            'test_attr'
        )

    @testErrorIsNotRaised
    def test_correct_percentage(self):
        BasePopulate._checkPercentageDefinition(0.5, 'test_attr')

# ---- _checkMinMaxValue -------------------------------------------------------
class TestCheckMinMaxValue(TestCase):
    def test_min_greater_than_max(self):
        self.assertRaises(
            ValueError,
            BasePopulate._checkMinMaxValue,
            5,
            3
        )

    def test_negative_values(self):
        self.assertRaises(
            ValueError,
            BasePopulate._checkMinMaxValue,
            1,
            -1
        )

        self.assertRaises(
            ValueError,
            BasePopulate._checkMinMaxValue,
            -1,
            1
        )

    @testErrorIsNotRaised
    def test_correct_percentage(self):
        BasePopulate._checkMinMaxValue(1, 2)

# ---- randomTrue --------------------------------------------------------------
class TestRandomTrue(TestCase):
    @patch(
        'backend.models.populate.BasePopulate.createRandomFloat',
        return_value=0.5
    )
    def test_get_true(self, mock_createRandomFloat):
        self.assertTrue(BasePopulate.randomTrue(0.6))

    @patch(
        'backend.models.populate.BasePopulate.createRandomFloat',
        return_value=0.5
    )
    def test_get_false(self, mock_createRandomFloat):
        self.assertFalse(BasePopulate.randomTrue(0.4))

# ---- _getPopulateFuncWithTypeName --------------------------------------------
class TestGetPopulateFuncWithTypeName(TestCase):
    def setUp(self):
        self.bp = BasePopulate(int)

    def test_func_not_implemented_yet(self):
        self.assertRaises(
            NotImplementedYet,
            self.bp._getPopulateFuncWithTypeName,
            "test"
        )

    def test_func_matches_type(self):
        self.assertEqual(
            self.bp._getPopulateFuncWithTypeName("int").__name__,
            "createRandomInt"
        )

# ---- createRandomInt ---------------------------------------------------------
# NOTE: This function only calls other functions and is therefore not tested!

# ---- createRandomFloat -------------------------------------------------------
# NOTE: This function only calls other functions and is therefore not tested!

# ---- _createUpperBorderForMaximalDigits --------------------------------------
class TestCreateUpperBorderForMaximalDigits(TestCase):
    def test_max_digits_smaller_zero(self):
        self.assertRaises(
            ValueError,
            BasePopulate._createUpperBorderForMaximalDigits,
            -1
        )

    def test_max_digits_zero(self):
        self.assertEqual(BasePopulate._createUpperBorderForMaximalDigits(0), 0)

    def test_max_digits_greater_zero(self):
        self.assertEqual(BasePopulate._createUpperBorderForMaximalDigits(1), 9)

# ---- createRandomDecimal -----------------------------------------------------
class TestCreateRandomDecimal(TestCase):
    @patch(
        'backend.models.populate.BasePopulate.createRandomInt',
        return_value=22
    )
    def test_decimal_with_whole_numbers(self, mock_createRandomInt):
        self.assertEqual(
            BasePopulate.createRandomDecimal(4, 2),
            Decimal('22.22')
        )

    @patch(
        'backend.models.populate.BasePopulate.createRandomInt',
        return_value=2
    )
    def test_decimal_with_leading_zero(self, mock_createRandomInt):
        self.assertEqual(
            BasePopulate.createRandomDecimal(3, 2),
            Decimal('2.02')
        )

    def test_decimal_places(self):
        max_digits = 5
        decimal_places = 2
        decimal_string =\
            f"{BasePopulate.createRandomDecimal(max_digits, decimal_places)}"

        self.assertEqual(len(decimal_string.split(".")[1]), decimal_places)

# ---- createRandomDatetime ----------------------------------------------------
# NOTE: This function only calls other functions and is therefore not tested!

# ---- createRandomDatetimeBetween ---------------------------------------------
# NOTE: This function only calls other functions and is therefore not tested!

# ---- createRandomDate --------------------------------------------------------
# NOTE: This function only calls other functions and is therefore not tested!

# ---- createRandomDateBetween -------------------------------------------------
# NOTE: This function only calls other functions and is therefore not tested!

# ---- createRandomTime --------------------------------------------------------
# NOTE: This function only calls other functions and is therefore not tested!

# ---- _shortenStringToMaxLength -----------------------------------------------
class TestShortenStringToMaxLength(TestCase):
    def setUp(self):
        self.string_to_shorten = "this text is here to be shortened"

    def test_text_smaller_than_max_length(self):
        self.assertEqual(
            BasePopulate._shortenStringToMaxLength(self.string_to_shorten, 35),
            self.string_to_shorten
        )

    def test_text_greater_than_max_length(self):
        self.assertEqual(
            BasePopulate._shortenStringToMaxLength(self.string_to_shorten, 10),
            "this text "
        )

# ---- _createRandomString -----------------------------------------------------
class TestCreateRandomString(TestCase):
    def test_random_string(self):
        max_length = 30
        random_string = BasePopulate._createRandomString(max_length)

        self.assertTrue(len(random_string) > 0)
        self.assertTrue(len(random_string) <= max_length)

    def test_random_string_if_max_length_smaller_five(self):
        max_length_smaller_five = 3
        random_string = BasePopulate._createRandomString(
            max_length_smaller_five
        )

        self.assertTrue(len(random_string) == max_length_smaller_five)

# ---- createRandomStr ---------------------------------------------------------
class TestCreateRandomStr(TestCase):
    @patch(
        'backend.models.populate.BasePopulate._createRandomString',
        return_value="test"
    )
    def test_random_string_is_smaller_than_min_length(
        self,
        mock_createRandomString
    ):
        self.assertEqual(BasePopulate.createRandomStr(6, 8), "testtest")

# ---- createRandomEmail -------------------------------------------------------
# NOTE: This function only calls other functions and is therefore not tested!

# ---- createRandomBool --------------------------------------------------------
class TestCreateRandomBool(TestCase):
    def test_get_none(self):
        self.assertIsNone(BasePopulate.createRandomBool(True, 1.0))

    @patch(
        'backend.models.populate.BasePopulate.FAKE.boolean',
        return_value=True
    )
    def test_get_bool(self, mock_fakeBoolean):
        self.assertTrue(BasePopulate.createRandomBool(chance_for_none=0.0))

# ---- createRandomData --------------------------------------------------------
# NOTE: This function only calls other functions and is therefore not tested!

# ---- _createRandomListAndDict ------------------------------------------------
class TestCreateRandomListAndDict(TestCase):
    @patch(
        'random.choice',
        return_value=int
    )
    @patch(
        'backend.models.populate.BasePopulate.populate',
        return_value=2
    )
    def test_create_random_list_and_dict(self, mock_choice, mock_populate):
        random_data_list, random_data_dict =\
            BasePopulate._createRandomListAndDict(1,1)

        self.assertListEqual(random_data_list, [2])
        self.assertDictEqual(random_data_dict, {"key_1": 2})

# ---- createRandomList --------------------------------------------------------
# NOTE: This function only calls other functions and is therefore not tested!

# ---- createRandomDict --------------------------------------------------------
# NOTE: This function only calls other functions and is therefore not tested!

# ---- createRandomJSON --------------------------------------------------------
class TestCreateRandomJSON(TestCase):
    @patch(
        'backend.models.populate.BasePopulate.createRandomData',
        return_value=2
    )
    def test_int_json(self, mock_createRandomInt):
        self.assertEqual(BasePopulate.createRandomJSON(), '2')

    @patch(
        'backend.models.populate.BasePopulate.createRandomData',
        return_value=Decimal('2.2')
    )
    def test_decimal_json(self, mock_createRandomDecimal):
        self.assertEqual(BasePopulate.createRandomJSON(), '"2.2"')

    @patch(
        'backend.models.populate.BasePopulate.createRandomData',
        return_value=datetime(1984, 7, 10, 22, 23, 51)
    )
    def test_datetime_json(self, mock_createRandomDatetime):
        self.assertEqual(
            BasePopulate.createRandomJSON(),
            '"1984-07-10T22:23:51"'
        )

# ---- _createMetaAttrName -----------------------------------------------------
class TestCreateMetaAttrName(TestCase):
    def test_create_meta_attr_name(self):
        self.assertEqual(BasePopulate._createMetaAttrName("test"), "meta__test")

# ---- _createMetaAttrListForFunc ----------------------------------------------
class TestCreateMetaAttrListForFunc(TestCase):
    def setUp(self):
        self.meta_attr_list = ["meta__attr_1", "meta__attr_2"]

    def test_meta_attr_list(self):
        def testFunc(attr_1, attr_2):
            pass

        self.assertListEqual(
            BasePopulate._createMetaAttrListForFunc(testFunc),
            self.meta_attr_list
        )

    def test_ignore_default_params_for_meta_attr_list(self):
        def testArgs(attr_1, attr_2, *args):
            pass

        def testKwargs(attr_1, attr_2, **kwargs):
            pass

        def testSelf(self, attr_1, attr_2):
            pass

        def testCls(cls, attr_1, attr_2):
            pass

        for testFunc in (testArgs, testKwargs, testSelf, testCls):
            self.assertListEqual(
                BasePopulate._createMetaAttrListForFunc(testFunc),
                self.meta_attr_list
            )

# ---- _checkAndCreateMetaAttrs ------------------------------------------------
class TestCheckAndCreateMetaAttrs(TestCase):
    def setUp(self):
        def testFunc(attr_1, attr_2):
            pass

        self.bp = BasePopulate(int)
        self._checkAndCreateMetaAttrs =\
            lambda **kwargs: self.bp._checkAndCreateMetaAttrs(
                testFunc,
                **kwargs
            )

    def test_incorrect_meta_attrs(self):
        self.assertRaises(
            ValueError,
            self._checkAndCreateMetaAttrs,
            meta__attr_1='test1',
            meta__attr_2='test2',
            meta__attr_3='test3'
        )

    def test_correct_meta_attrs(self):
        self._checkAndCreateMetaAttrs(
            meta__attr_1='test1',
            meta__attr_2='test2'
        )

        self.assertEqual(self.bp.meta__attr_1, 'test1')
        self.assertEqual(self.bp.meta__attr_2, 'test2')

# ---- _createCustomAttrDict ---------------------------------------------------
class TestCreateCustomAttrDict(TestCase):
    def setUp(self):
        def testFunc(attr_1, attr_2):
            pass

        self.bp = BasePopulate(int)
        self._createCustomAttrDict =\
            lambda: self.bp._createCustomAttrDict(testFunc)

    def test_no_attrs(self):
        self.assertDictEqual(self._createCustomAttrDict(), {})

    def test_one_attrs(self):
        self.bp.meta__attr_1 = 'test1'

        self.assertDictEqual(
            self._createCustomAttrDict(),
            {"attr_1": "test1"}
        )

    def test_two_attrs(self):
        self.bp.meta__attr_1 = 'test1'
        self.bp.meta__attr_2 = 'test2'

        self.assertDictEqual(
            self._createCustomAttrDict(),
            {"attr_1": "test1", "attr_2": "test2"}
        )

# ---- _checkCustomAndMetaAttrs ------------------------------------------------
class TestCheckCustomAndMetaAttrs(TestCase):
    def setUp(self):
        self.bp = BasePopulate(int)

        self._checkCustomAndMetaAttrs =\
            lambda **kwargs: self.bp._checkCustomAndMetaAttrs(
                ["attr_1", "attr_2"],
                **kwargs
            )

    def test_incorrect_attr(self):
        self.assertRaises(
            ValueError,
            self._checkCustomAndMetaAttrs,
            attr_3='test3'
        )

    def test_incorrect_attr_type(self):
        self.assertRaises(
            TypeError,
            self._checkCustomAndMetaAttrs,
            meta__attr_2='test3'
        )

    @testErrorIsNotRaised
    def test_correct_attrs(self):
        self._checkCustomAndMetaAttrs(attr_1='test1', meta__attr_1={'test': 1})

# ---- _createCustomAndMetaAttrs -----------------------------------------------
class TestCreateCustomAndMetaAttrs(TestCase):
    def setUp(self):
        self.bp = BasePopulate(int)

        self._createCustomAndMetaAttrs =\
            lambda **kwargs: self.bp._createCustomAndMetaAttrs(
                ["attr_1", "attr_2"],
                **kwargs
            )

    def test_attr_existing(self):
        self.bp.attr_1 = 'test1'

        self.assertRaises(
            ValueError,
            self._createCustomAndMetaAttrs,
            attr_1='test1'
        )

    def test_create_attrs_with_not_provided(self):
        self._createCustomAndMetaAttrs()

        self.assertEqual(self.bp.attr_1, NOT_PROVIDED)
        self.assertEqual(self.bp.attr_2, NOT_PROVIDED)
        self.assertEqual(self.bp.meta__attr_1, NOT_PROVIDED)
        self.assertEqual(self.bp.meta__attr_2, NOT_PROVIDED)

    def test_create_attrs_with_custom_value(self):
        self._createCustomAndMetaAttrs(attr_1='test1', meta__attr_1={'test': 1})

        self.assertEqual(self.bp.attr_1, 'test1')
        self.assertDictEqual(self.bp.meta__attr_1, {'test': 1})

class TestBasePopulateMethods(TestCase):
    def setUp(self):
        self.type_to_populate = int
        self.populated_int = 1
        self.custom_kwargs = {
            "meta__min_value": self.populated_int,
            "meta__max_value": self.populated_int
        }
        self.bp = BasePopulate(self.type_to_populate, **self.custom_kwargs)

    # ---- populate ------------------------------------------------------------
    def test_populate(self):
        self.assertEqual(self.bp.populate(), self.populated_int)

    # ---- populateMany --------------------------------------------------------
    @patch(
        'backend.models.populate.BasePopulate.createRandomInt',
        return_value=1
    )
    def test_populate_many(self, mock_createRandomInt):
        self.assertListEqual(self.bp.populateMany(), [1])

    # ---- populateWithData ----------------------------------------------------
    def test_populate_with_data(self):
        self.assertListEqual(
            BasePopulate.populateWithData(
                self.type_to_populate,
                [self.custom_kwargs]
            ),
            [1]
        )