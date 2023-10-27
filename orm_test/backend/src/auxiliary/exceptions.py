class NonExistentGroupError(Exception):
    pass

class NotUpdatableError(Exception):
    pass

class NotValidIdError(Exception):
    pass

class MissingAttributeError(Exception):
    pass

################################################################################
##### populate exceptions ######################################################
################################################################################
class IncompatibleValidatorList(Exception):
    pass

class NotImplementedYet(Exception):
    pass

class NotConfigured(Exception):
    pass

class ResultContradictsConfiguration(Exception):
    pass