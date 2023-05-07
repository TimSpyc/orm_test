
class UpdateCacheAttributeCallMeta(type):
    """
    A meta-class that automatically calls the `updateCache` method when a method
    of the class is called. The `updateCache` method should be defined in the class
    that uses this meta-class.
    """
    def __new__(cls, name, bases, dct):
        for attr_name, attr_value in dct.items():
            if callable(attr_value) and attr_name not in {"__init__", "__new__"}:
                def new_method(self, *args, **kwargs):
                    self.updateCache()
                    return attr_value(self, *args, **kwargs)
                dct[attr_name] = new_method
        return super(UpdateCacheAttributeCallMeta, cls).__new__(cls, name, bases, dct)

class UpdateCacheAttributeChangeMeta(type):
    """
    A meta-class that automatically calls the `updateCache` method when an attribute
    of the class is changed. The `updateCache` method should be defined in the class
    that uses this meta-class.
    """
    def __new__(cls, name, bases, dct):
        def new_setattr(self, name, value):
            super(self.__class__, self).__setattr__(name, value)
            self.updateCache()

        dct['__setattr__'] = new_setattr
        return super(UpdateCacheAttributeChangeMeta, cls).__new__(cls, name, bases, dct)

