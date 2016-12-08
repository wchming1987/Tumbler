#!/usr/bin/env python
# -*- coding=utf-8 -*-

import json
from bson import json_util

import tornado.web

from doubanAPI import DoubanAPI


class BaseHandler(tornado.web.RequestHandler):
    def __init__(self, *args, **kwargs):
        # 继承于 tornado.web.RequestHandler
        tornado.web.RequestHandler.__init__(self, *args, **kwargs)

        self.db = self.application.db

    def __exit__(self):
        self.db.close()

class BooksHandler(BaseHandler):
    def get(self):
        print('---------------------------------')
        # 获取书籍列表
        books = []

        collection = self.db['books']
        for item in collection.find():
            print json.dumps(item, default=json_util.default).decode("unicode_escape")
            books.append(item)

        self.write(json.dumps(books, default=json_util.default).decode("unicode_escape"))
        print('---------------------------------')


class BookHandler(BaseHandler):
    def get(self, *args, **kwargs):
        print('---------------------------------')
        # 获取 ISBN
        isbn13 = ''
        if len(args[0]) == 13 and args[0].isdigit():
            isbn13 = args[0]
        if len(args[0]) == 10 and args[0].isdigit():
            ## 旧版的 ISBN，补全前三位的商品编号
            isbn13 = '978' + args[0]
        else:
            self.write('')
        print('ISBN:[{isbn13}]'.format(isbn13=isbn13))

        # 获取书籍信息
        collection = self.db['books']
        book = collection.find_one({'isbn13': isbn13})
        ##book = json.dumps(book, default=json_util.default).decode("unicode_escape")
        print('book is null:[{wether}]'.format(wether=(None == book)))

        ## 如果数据库中没有相关数据，则去获取豆瓣数据补充到数据库中
        if None == book:
            apiClient = DoubanAPI()
            bookInfo = apiClient.getBook(isbn13)
            if len(bookInfo) == 0:
                print("访问豆瓣API获取书籍数据失败")
                exit -1

            ## 插入书籍信息
            bookJson = json.loads(bookInfo)
            collection = self.db['books']
            result = collection.insert({
                'isbn10': bookJson['isbn10'],
                'isbn13': bookJson['isbn13'],
                'name': bookJson['title'],
                'author': bookJson['author'],
                'publisher': bookJson['publisher'],
                'pubdate': bookJson['pubdate'],
                'image': bookJson['images']['medium'],
                "doubanGrade": bookJson['rating']['average'],
                'isBought': False,
                'isLending': False
            })

            book = collection.find_one({'isbn13': isbn13})

        book = json.dumps(book, default=json_util.default).decode("unicode_escape")
        print('book:[{book}]'.format(book=book))

        self.write(book)
        print('---------------------------------')

    def post(self, *args, **kwargs):
        print('---------------------------------')


class BuyBookHandler(BaseHandler):
    def post(self, *args, **kwargs):
        print('---------------------------------')

        ## 获取 ISBN
        isbn = args[0]
        if len(isbn) == 13 and isbn.isdigit():
            isbn13 = isbn
        if len(isbn) == 10 and isbn.isdigit():
            ## 旧版的 ISBN，补全前三位的商品编号
            isbn13 = '978' + isbn
        else:
            self.write('')
        print('ISBN:[{isbn13}]'.format(isbn13=isbn13))

        ## 获取书籍信息
        collection = self.db['books']
        result = collection.update_one({'isbn13': isbn13}, {"$set":{'isBought': True}})

        book = collection.find_one({'isbn13': isbn13})
        book = json.dumps(book, default=json_util.default).decode("unicode_escape")

        self.write(book)

        print('---------------------------------')


class MattersHandler(BaseHandler):
    def get(self):
        print('---------------------------------')
        # 获取提醒列表
        matters = []

        collection = self.db['matters']
        for item in collection.find():
            print json.dumps(item, default=json_util.default).decode("unicode_escape")
            matters.append(item)

        self.write(json.dumps(matters, default=json_util.default).decode("unicode_escape"))
        print('---------------------------------')


class MatterHandler(BaseHandler):
    def get(self, *args, **kwargs):
        print('---------------------------------')
        # 获取 id
        id = args[0]
        print('id:[{id}]'.format(id=id))

        # 获取书籍信息
        collection = self.db['books']
        book = collection.find_one({'_id': id})
        matter = json.dumps(book, default=json_util.default).decode("unicode_escape")
        print('matter:[{matter}]'.format(matter=matter))

        self.write(matter)
        print('---------------------------------')

    def post(self, *args, **kwargs):
        print('---------------------------------')

        # 插入提醒信息
        collection = self.db['matters']
        result = collection.insert({
            'topic': self.get_argument("topic"),
            'address': self.get_argument("address"),
            'fromDateTime': self.get_argument("fromDateTime"),
            'toDateTime': self.get_argument("toDateTime"),
            'noticeBefore': self.get_argument("noticeBefore")
        })

        print('---------------------------------')

