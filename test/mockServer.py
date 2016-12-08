#!/usr/bin/python
# -*- coding=utf-8 -*-

import time
import json
import sys
import urllib
import urllib2

import tornado.autoreload
import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado import gen
from tornado.httpclient import AsyncHTTPClient, HTTPRequest
from tornado.options import define, options


# 希望返回成功还是失败
#  1 - 成功
# -1 - 失败
is_success = 1

# 代付结果通知回调地址
callBackUrl = 'http://10.3.200.6:9002'

# 服务端口
define('port', default=9555, help='run on the given port', type=int)

reload(sys)
sys.setdefaultencoding('utf-8')


class RepayHandler(tornado.web.RequestHandler):
    orderId = ''

    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        self.post(args, kwargs)

    @tornado.gen.coroutine
    def post(self, *args, **kwargs):
        #body = self.request.body.replace("'", '"')
        #body_args = json.loads(body[7: ])

        #self.orderId = body_args['order_id']

        params = self.get_argument('params')
        print('params:[' + params + ']')

        args = json.loads(params)
        self.orderId = args['order_id']
        print('order_id:[' + self.orderId + ']')

        respone = {'code': 2000}
        self.write(json.dumps(respone))

        self.call_back()

    @tornado.gen.coroutine
    def call_back(self):
        yield gen.sleep(1)

        request = {}

        service_body = {}
        if is_success == 1:
            service_body['RCD'] = '0000'
            service_body['RDESC'] = '支付成功'
            service_body['ORDERID'] = self.orderId
        else:
            service_body['RCD'] = '0108'
            service_body['RDESC'] = '支付失败'
            service_body['ORDERID'] = self.orderId

        request['serviceHeader'] = {'serviceId': 'TFCRepayresultNotice'}
        request['serviceBody'] = service_body

        http_request = HTTPRequest(url=callBackUrl, method='POST', body=json.dumps(request, ensure_ascii=False))
        http_client = AsyncHTTPClient()
        http_client.fetch(http_request)


class CollectHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.post(args, kwargs)

    def post(self, *args, **kwargs):
        #body = self.request.body.replace("'", '"')
        #body_args = json.loads(body[7: ])
        #self.orderId = body_args['repayment_id']

        params = self.get_argument('params')
        print('params:[' + params + ']')

        args = json.loads(params)

        respone = {}

        result = {}
        result['account_name'] = args['account_name']
        result['card_num'] = args['card_num']
        result['identity_id'] = args['identity_id']
        result['repayment_date'] = args['repayment_date']
        result['repayment_id'] = args['repayment_id']
        result['transaction_amount'] = args['transaction_amount']
        #result['response_code'] = '96'
        #result['response_status'] = '0'
        #result['status'] = 1
        #result['purpose'] = '联机正常扣款'

        if is_success == 1:
            result['purpose'] = '联机正常扣款'
            result['response_code'] = '00'
            result['response_status'] = '00'
            result['status'] = 1
        else:
            result['purpose'] = '联机扣款失败'
            result['response_code'] = '96'
            result['response_status'] = '05'
            result['status'] = 2

        respone['code'] = 2000
        respone['result'] = result

        self.write(json.dumps(respone, ensure_ascii=False))


if __name__ == '__main__':
    handlers = [
        (r'/repay', RepayHandler),
        (r'/collect', CollectHandler),
    ]

    webApp = tornado.web.Application(handlers)
    httpServer = tornado.httpserver.HTTPServer(webApp)
    httpServer.listen(options.port)

    loop = tornado.ioloop.IOLoop.instance()
    tornado.autoreload.start(loop)
    loop.start()
