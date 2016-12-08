#!/usr/bin/python
# -*- coding=utf-8 -*-

import ConfigParser
import logging
import os.path
import sys

import tornado.autoreload
import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado.options import define, options

import pymongo

from handlers import *

reload(sys)
sys.setdefaultencoding('utf-8')

define('port', default=12000, help='run on the given port', type=int)
define('loglevel', default='debug', help='log level')
define('debug', default=True, help='run in debug mode')


class DBApplication(tornado.web.Application):
    def __init__(self, handlers, **settings):
        tornado.web.Application.__init__(self, handlers, **settings)

        try:
            config = ConfigParser.SafeConfigParser()
            path = os.path.join(os.path.dirname(__file__), 'config', 'db.ini')
            config.read(path)

            self.conn = pymongo.MongoClient(
                config.get('database', 'dbhost'),
                int(config.get('database', 'dbport'))
            )
            self.db = self.conn.get_database(config.get('database', 'dbname'))
            self.db.authenticate(
                config.get('database', 'dbuser'),
                config.get('database', 'dbpassword')
            )
        except Exception, ex:
            print ex
            exit(-1)

handlers = [
    (r'/books', BooksHandler),
    (r'/book/(.*)/buy', BuyBookHandler),
    (r'/book/(.*)', BookHandler),
    (r'/matters', MattersHandler),
    (r'/matter/(.*)', MatterHandler),
    (r'/matter', MatterHandler),
]

settings = {
    # 设置 cookie_secret
    # 'cookie_secret': 'FASDFA12psaldQWRJLSDFJL87123jHAFu0',
    # 设置静态文件夹，此处设置为了 ./static
    # 就可以直接访问 http://xxxxxx:xxxx/static/* 的文件了
    # 'static_path': os.path.join(os.path.dirname(__file__), 'static'),
    # 'template_path': os.path.join(os.path.dirname(__file__), 'templates'),
    'debug': options.debug,
    # 设置登录页面
    # 'login_url': '/login.html',
    # 是否防跨域 POST （具体见文档）
    #"xsrf_cookies": True,
    # 关掉自动 escape
    "autoescape": None
}

if __name__ == '__main__':
    ## setup log
    tornado.options.options.logging = options.loglevel
    tornado.options.options.log_to_stderr = True
    tornado.options.options.log_file_prefix = os.path.join(os.path.dirname(__file__), 'log', 'run.log')
    tornado.options.options.log_file_max_size = 1000000
    tornado.options.parse_command_line()

    logging.info('---------------- Begin Start Server... ----------------')
    logging.debug('LogLevel:[%s]' % tornado.options.options.logging)
    logging.debug('LogFile:[%s]' % tornado.options.options.log_file_prefix)

    webApp = DBApplication(handlers, **settings)
    httpServer = tornado.httpserver.HTTPServer(webApp)
    httpServer.listen(options.port)

    loop = tornado.ioloop.IOLoop.instance()
    tornado.autoreload.start(loop)
    loop.start()
