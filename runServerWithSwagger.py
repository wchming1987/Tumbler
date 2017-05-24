#!/usr/bin/python
# -*- coding=utf-8 -*-

import ConfigParser
import os
import signal
import time

import tornado.httpserver
import tornado.ioloop

from tornado_swagger import swagger

from lib import log

from handler.Book import BooksHandler
from handler.Reminder import RemindersHandler

import pymongo

MAX_WAIT_SECONDS_BEFORE_SHUTDOWN = 5

swagger.docs()

@swagger.model()
class PropertySubclass:
    def __init__(self, sub_property=None):
        self.sub_property = sub_property

# class ItemHandler(GenericApiHandler):
#     @swagger.operation(nickname='get')
#     def get(self, arg):
#         """
#             @rtype: L{Item}
#             @description: get information of a item
#             @notes:
#                 get a item,
#
#                 This will be added to the Implementation Notes.It lets you put very long text in your api.
#         """
#         self.finish_request(items[arg].format_http())
#
#     @swagger.operation(nickname='delete')
#     def delete(self, arg):
#         """
#             @description: delete a item
#             @notes:
#                 delete a item in items
#
#                 This will be added to the Implementation Notes.It lets you put very long text in your api.
#         """
#         del items[arg]
#         self.finish_request("success")
#
#
# class ItemOptionParamHandler(GenericApiHandler):
#     @swagger.operation(nickname='create')
#     def post(self, arg1, arg2=''):
#         """
#         @return 200: case is created
#         """
#         print("ProjectHandler.post: %s -- %s -- %s" % (arg1, arg2, self.request.full_url()))
#         fs = open("/home/swagger/tornado-rest-swagger/%s/%s" % (arg1, arg2), "wb")
#         fs.write(self.request.body)
#         self.write("success")
#
#
# class ItemQueryHandler(GenericApiHandler):
#     @swagger.operation(nickname='query')
#     def get(self):
#         """
#            @param property1:
#            @type property1: L{string}
#            @in property1: query
#            @required property1: False
#
#            @param property2:
#            @type property2: L{string}
#            @in property2: query
#            @required property2: True
#            @rtype: L{Item}
#            @notes: GET /item?property1=1&property2=1
#         """
#         property1 = self.get_query_argument("property1", None)
#         property2 = self.get_query_argument("property2", None)
#
#         res = []
#         if property1 is None:
#             for key, value in items.iteritems():
#                 if property2 is None:
#                     res.append(value.format_http())
#                 elif value.property2 == property2:
#                     res.append(value.format_http())
#         elif items.has_key(property1):
#             if items.get(property1).property2 == property2:
#                 res.append(items.get(property1).format_http())
#
#         self.finish_request(res)


def make_app():
    ## TODO: 数据库、日志 等连接需要封装
    try:
        config = ConfigParser.SafeConfigParser()
        path = os.path.join(os.path.dirname(__file__), 'config', 'db.conf')
        config.read(path)

        connection = pymongo.MongoClient(
            config.get('database', 'dbhost'),
            int(config.get('database', 'dbport'))
        )
        database = connection.get_database(config.get('database', 'dbname'))
        database.authenticate(
            config.get('database', 'dbuser'),
            config.get('database', 'dbpassword')
        )
    except Exception, ex:
        print ex
        exit(-1)

    ## TODO: 需要开发自动识别 Handler 类
    return swagger.Application([
        #(r"/item", ItemQueryHandler),
        (r"/books", BooksHandler, dict(database=database)),
        #(r"/books/([^/]+)", ItemHandler),
        #(r"/items/([^/]+)/cases/([^/]+)", ItemOptionParamHandler),
        (r"/reminders", RemindersHandler, dict(database=database)),
    ])


def sig_handler(sig, frame):
    log.logger.warning('Caught signal: %s', sig)
    tornado.ioloop.IOLoop.instance().add_callback_from_signal(shutdown)


def shutdown():
    log.logger.info('Stopping http server')

    webApp.stop()  # 不接收新的 HTTP 请求

    log.logger.info('Will shutdown in %s seconds ...', MAX_WAIT_SECONDS_BEFORE_SHUTDOWN)
    io_loop = tornado.ioloop.IOLoop.instance()

    deadline = time.time() + MAX_WAIT_SECONDS_BEFORE_SHUTDOWN

    def stop_loop():
        now = time.time()
        if now < deadline and (io_loop._callbacks or io_loop._timeouts):
            io_loop.add_timeout(now + 1, stop_loop)
        else:
            io_loop.stop()  # 处理完现有的 callback 和 timeout 后，可以跳出 io_loop.start() 里的循环
            log.logger.info('Shutdown')

    stop_loop()


if __name__ == "__main__":
    webApp = make_app()
    webApp.listen(711)

    signal.signal(signal.SIGTERM, sig_handler)
    signal.signal(signal.SIGINT, sig_handler)

    tornado.ioloop.IOLoop.current().start()

    log.logger.info('Exit')
