from pprint import pformat

class Struct(object):
    def __init__(self, **kwds):
        self.__dict__.update(**kwds)
    def __repr__(self):
        return pformat(vars(self))

