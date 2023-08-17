from backend.src.auxiliary import addPrefixToDict
from backend.src.manager import DerivativeConstelliumManager

def serializeDerivativeConstellium(
    derivative_constellium_manager_obj: DerivativeConstelliumManager
) -> dict:

    return {
        **dict(derivative_constellium_manager_obj), 
        **addPrefixToDict(
            dict(
                derivative_constellium_manager_obj.\
                project_manager
            ),
            'customer'
        ),

    }
