#!/usr/bin/python
# -*- coding=utf-8 -*-

import json
from bson import json_util

from tornado_swagger import swagger

from handler.GenericApiHandler import GenericApiHandler


class RemindersHandler(GenericApiHandler):
    @swagger.operation(nickname='list')
    def get(self):
        """
           @rtype: L{Reminder}
        """
        # 获取提醒列表
        reminders = []

        collection = self.database['reminder']
        if collection is not None:
            for reminder in collection.find():
                print json.dumps(reminder, default=json_util.default).decode("unicode_escape")
                reminders.append(reminder)

        self.write(json.dumps(reminders, default=json_util.default).decode("unicode_escape"))
        ###self.finish_request(reminders)

    @swagger.operation(nickname='create')
    def post(self):
        """
            @param body: create a item.
            @type body: L{Item}
            @in body: body
            @return 200: item is created.
            @raise 400: invalid input
        """
        if self.database is None:
            print('Error: db is None')

        # 插入提醒信息
        collection = self.database['reminder']
        result = collection.insert({
            'topic': self.param_args.get("topic"),
            'address': self.param_args.get("address"),
            'startDateTime': self.param_args.get("startDateTime"),
            'endDateTime': self.param_args.get("endDateTime"),
            "content": self.param_args.get("content"),
            'noticeBefore': self.param_args.get("noticeBefore")
        })

    def options(self):
        """
        I'm not visible in the swagger docs
        """
        self.finish_request("I'm invisible in the swagger docs")

