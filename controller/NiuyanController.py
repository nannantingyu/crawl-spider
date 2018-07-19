# -*- coding: utf-8 -*-
from Controller import Controller
import json, redis
from settings import redis_config

class NiuyanController(Controller):
    def __init__(self, topic="niuyan_hangqing"):
        super(NiuyanController, self).__init__(topic, 'niuyan_hangqing')
        self.r = redis.Redis(host=redis_config['host'], port=redis_config['port'])

    def run(self):
        for msg in self.consumer:
            try:
                print json.loads(msg.value.decode('utf-8'))
                self.r.publish("digita_currency", msg.value.decode('utf-8'))
            except:
                self.logger.error('Catch an exception.', exc_info=True)
