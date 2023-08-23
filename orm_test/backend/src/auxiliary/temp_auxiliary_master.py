import json
import datetime
from dateutil.relativedelta import relativedelta

format_of_valid_14_digit_integer_date = '%Y%m%d%H%M%S'

################################################################################
##### Auxiliary functions! #####################################################
################################################################################
def isValidInt(int_value):
    # TODO #4836 docstring is missing; please explain your function
    try:
        int(int_value)
        return True
    except ValueError:
        return False


def isValidFloat(float_value):
    # TODO #4836 docstring is missing; please explain your function
    try:
        float(float_value)
        return True
    except ValueError:
        return False

def isValidList(list_value):
    # TODO #4836 docstring is missing; please explain your function
    try:
        if type(list_value) is list:
            return True
        else:
            is_list = json.loads(list_value)       
        if type(is_list) is not list:
            return False
        return True
    except:
        return False

def queryParamsIntoDict(request):
    '''
    The information from the url is returned in its basic form as dict.

    Parameters
    ----------
    request : rest_framework.request.Request
        Contains the query dict with the information passed via the url.

    Returns
    -------
    query_params_dict : dict
        Contains the information passed via the url in its basic form.
    '''
    query_params_dict = dict(request.query_params)

    if len(query_params_dict) > 0:
        
        temp_query_params_dict = dict()
        
        # TODO Possibly recognize and convert additional data types 
        
        for key, value in query_params_dict.items():
            
            if isValidInt(value[0]):
                temp_query_params_dict[key] = int(value[0])
            elif isValidFloat(value[0]):
                temp_query_params_dict[key] = float(value[0])
            elif isValidList(value[0]):
                temp_query_params_dict[key] = json.loads(value[0])
            else:
                temp_query_params_dict[key] = value[0]

        return temp_query_params_dict
    
    return query_params_dict    

def convertDatetimeObjectTo14DigitInteger(
        datetime_object,
        stringformat=format_of_valid_14_digit_integer_date):

    # TODO das kann dann auch richtig geschrieben werden? ohne string vergleich
    if str(datetime_object) == 'NaT' or datetime_object is None:
        return None
    
    if datetime_object == '-':
        return None

    try:
        return int(datetime_object.strftime(stringformat))

    except Exception as e:
        # print(e, 'given object could not be converted to number')

        # return datetime_object
        return None

def getDate(date=None):
    """
    This function creates a date integer if the kwarg is None. By default
    this argument is None. If it is not None the algorithm checks if the date
    is of type integer and if date is as long as 14 digits. If this is true the
    14 digit integer is returned otherwise a ValueError raises

    Args:
        date (int, optional): int value of a certain date. Defaults to None.
        Input:  Date (e.g. 20200110121500) (default = None)
    Raises:
        ValueError: if the given input isn't of type int or the length isn't 14
        this error raises.

    Returns:
        int: date with a 14 digit number with this format: YYYYMMDDhhmmss
    """

    # TODO #3094 plausibility check of int in getDate() is missing input like 20223540000000 is now interpreted as valid

    if date is None:
        date = convertDatetimeObjectTo14DigitInteger(datetime.datetime.now())

    convert14DigitIntegerIntoDateTimeObject(date)

    return date

def createDateTimeObjectFromString(
    date_string,
    format=format_of_valid_14_digit_integer_date
):

    # check if everything is defined at this position
    # man kann auch andere valide datetime formate wählen
    # write docstring
    # write tsets

    return datetime.datetime.strptime(date_string, format)

def convert14DigitIntegerIntoDateTimeObject(date_integer_to_convert):
    """
    This function is able to convert a given 14 digit integer number to
    a datetimeobject, with the respective properties. The Number is transformed
    to the datetime object if the string format corresponds to the number itself.
    Since the format is defined globally only 14 digit and no other smaller 
    numbers are valid.

    Invalid entries; e.g.:
        - 20223040000000
        - '20223040000000'
        - 2022
        - 202206 
        - ...

    Args:
        date_integer_to_convert (int): standard integer format for date

    Raises:
        ValueError: raises if the given number is not standard format

    Returns:
        datetime object: the datetimeobject of the given integer number
    """

    try:

        datetime_obj = createDateTimeObjectFromString(
            str(date_integer_to_convert),
            format=format_of_valid_14_digit_integer_date
        )
        return datetime_obj

    except Exception:
        raise ValueError(f"""
            Given integer: {date_integer_to_convert} is not a valid date. 
            Please check for typos!""")

def timedeltaFromGivenDateInteger(date, delta, increment='days'):
    # function can be enhanced to handle datetimeobjects directly
    # NOTE negative values for delta are also a valid input! but only integeres!

    # this list describes the valid increments
    list_of_valid_increments = [
        'years',
        'months',
        'days',
        'weeks',
        'hours',
        'minutes',
        'seconds',
        'microseconds',
    ]

    try:
        # supposedly given date is an integer!
        date = getDate(date)

    except Exception as e:
        print('Given date is of wrong format. It is not possible to calculate delta: ', e)
        return

    datetime_obj = convert14DigitIntegerIntoDateTimeObject(date)

    # figure out which module is needed to calculate the delta of time:
    if increment not in list_of_valid_increments:
        raise ValueError(f"""
            Given time_increment "{increment}" is not supported. 
            Check documentaion."""
                         )

    if increment == 'years':
        datetime_obj += relativedelta(years=delta)
    elif increment == 'months':
        datetime_obj += relativedelta(months=delta)
    elif increment == 'days':
        datetime_obj += relativedelta(days=delta)
    elif increment == 'weeks':
        datetime_obj += relativedelta(weeks=delta)
    elif increment == 'seconds':
        datetime_obj += relativedelta(seconds=delta)
    elif increment == 'microseconds':
        datetime_obj += relativedelta(microseconds=delta)
    elif increment == 'minutes':
        datetime_obj += relativedelta(minutes=delta)
    elif increment == 'hours':
        datetime_obj += relativedelta(hours=delta)
    elif increment == 'weeks':
        datetime_obj += relativedelta(weeks=delta)

    date_delta_integer = convertDatetimeObjectTo14DigitInteger(datetime_obj)

    return date_delta_integer