#!/usr/bin/python
# -*- coding=utf-8 -*-

import json
from bson import json_util

from tornado_swagger import swagger

from handler.GenericApiHandler import GenericApiHandler


class BooksHandler(GenericApiHandler):
    @swagger.operation(nickname='list')
    def get(self):
        """
           @rtype: L{Book}
        """
        print('---------------------------------')
        # 获取书籍列表
        books = []

        collection = self.db['books']
        for item in collection.find():
            print json.dumps(item, default=json_util.default).decode("unicode_escape")
            books.append(item)

        self.write(json.dumps(books, default=json_util.default).decode("unicode_escape"))
        print('---------------------------------')

        self.finish_request(books)

    @swagger.operation(nickname='create')
    def post(self):
        """
            @param body: create a item.
            @type body: L{Item}
            @in body: body
            @return 200: item is created.
            @raise 400: invalid input
        """
        # property1 = self.json_args.get('property1')
        # item = Item.item_from_dict(self.json_args)
        # items[property1] = item
        # Item.test_classmethod()
        # self.finish_request(item.format_http())

        pass

    def options(self):
        """
        I'm not visible in the swagger docs
        """
        self.finish_request("I'm invisible in the swagger docs")

