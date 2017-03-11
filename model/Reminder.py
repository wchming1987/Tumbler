#!/usr/bin/env python
# -*- coding=utf-8 -*-

from tornado_swagger import swagger


@swagger.model
class Reminder:
    """
        @description:
            This is an example of a model class that has parameters in its constructor
            and the fields in the swagger spec are derived from the parameters to __init__.
        @notes:
            In this case we would have property1, name as required parameters and property3 as optional parameter.
        @property topic: Item description
        @ptype property3: L{PropertySubclass}
        @ptype property4: C{list} of L{PropertySubclass}
    """
    def __init__(self, id, topic=None, address=None, start_date_time=None, end_date_time=None, content=None, notice_before=None):
        self.id = id
        self.topic = topic
        self.address = address
        self.startDateTime = start_date_time
        self.endDateTime = end_date_time
        self.content = content
        self.noticeBefore = notice_before


