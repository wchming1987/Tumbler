#!/usr/bin/python
# -*- coding=utf-8 -*-

import ConfigParser
import logging
import os.path
import signal
import sys
import time

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

            signal.signal(signal.SIGTERM, self.sig_handler)
            signal.signal(signal.SIGINT, self.sig_handler)

        except Exception, ex:
            print ex
            exit(-1)

    def sig_handler(self, sig, frame):
        logging.warning('Caught signal: %s', sig)
        tornado.ioloop.IOLoop.instance().add_callback_from_signa(self.shutdown)

    def shutdown(self):
        logging.info('Stopping http server')
        self.stop()  # 不接收新的 HTTP 请求

        logging.info('Will shutdown in %s seconds ...', settings.MAX_WAIT_SECONDS_BEFORE_SHUTDOWN)
        io_loop = tornado.ioloop.IOLoop.instance()

        deadline = time.time() + settings.MAX_WAIT_SECONDS_BEFORE_SHUTDOWN

        def stop_loop():
            now = time.time()
            if now < deadline and (io_loop._callbacks or io_loop._timeouts):
                io_loop.add_timeout(now + 1, stop_loop)
            else:
                io_loop.stop()  # 处理完现有的 callback 和 timeout 后，可以跳出 io_loop.start() 里的循环
                logging.info('Shutdown')

        stop_loop()

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
    httpServer.bind(options.port)

    #loop = tornado.ioloop.IOLoop.instance()
    #tornado.autoreload.start(loop)
    #loop.start()

    tornado.ioloop.IOLoop.instance().start()

    logging.info('Exit')
