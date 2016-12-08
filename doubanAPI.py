#!/usr/bin/env python
# -*- coding=utf-8 -*-

import httplib2
import json

class DoubanAPI():
    def defaultAPI(self, url):
        client = httplib2.Http()

        response, content = client.request(url)
        result = bytes.decode(content)
        print('result:[{}]'.format(result))

        return result

    def getBook(self, isbn):
        apiURL = "https://api.douban.com/v2/book/isbn/" + isbn
        print("URL:[{}]".format(apiURL))

        result = self.defaultAPI(apiURL)

        return result






