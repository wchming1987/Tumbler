#!/usr/bin/python
# -*- coding=utf-8 -*-

from tornado_swagger import swagger

@swagger.model()
class Book:
    """
        @description:
            This is an example of a model class that has parameters in its constructor
            and the fields in the swagger spec are derived from the parameters to __init__.
        @notes:
            In this case we would have property1, name as required parameters and property3 as optional parameter.
        @property property3: Item description
        @ptype property3: L{PropertySubclass}
        @ptype property4: C{list} of L{PropertySubclass}
    """
    def __init__(self, ISBN, ISBN10=None, name=None):
        self.property1 = ISBN
        self.property2 = ISBN10
        self.property3 = name


