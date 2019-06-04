# -*- coding:utf-8 -*
from werobot import WeRoBot

myrobot = WeRoBot(token='token')


@myrobot.handler
def hello(message):
    return 'Hello World!'
