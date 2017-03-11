#!/usr/bin/python
# -*- coding=utf-8 -*-

import json

from tornado.web import RequestHandler, HTTPError

import pymongo

FORM_REPRESENTATION = ''
JSON_REPRESENTATION = 'application/json'

HTTP_BAD_REQUEST = 400
HTTP_FORBIDDEN = 403
HTTP_NOT_FOUND = 404


class GenericApiHandler(RequestHandler):
    """
    The purpose of this class is to take benefit of inheritance and prepare
    a set of common functions for
    the handlers
    """
    def __init__(self, application, request, **kwargs):
        self.database = None
        self.param_args = None

        super(GenericApiHandler, self).__init__(application, request, **kwargs)

    def initialize(self, database):
        self.database = database

    def prepare(self):
        if not (self.request.method == "GET" or self.request.method == "DELETE"):
            if self.request.headers.get("Content-Type") is not None:
                if self.request.headers["Content-Type"].startswith(JSON_REPRESENTATION):
                    try:
                        self.param_args = json.loads(self.request.body)
                    except (ValueError, KeyError, TypeError) as error:
                        raise HTTPError(HTTP_BAD_REQUEST,
                                        "Bad Json format [{}]".
                                        format(error))
                elif self.request.headers["Content-Type"].startswith(FORM_REPRESENTATION):
                    pass
                else:
                    pass

    def finish_request(self, json_object):
        self.write(json.dumps(json_object))
        self.set_header("Content-Type", JSON_REPRESENTATION)
        self.finish()
