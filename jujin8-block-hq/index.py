# -*- coding: utf-8 -*-
import os
import logging
import redis, json
import gevent
import re
from flask import Flask, render_template
from flask_sockets import Sockets

from dotenv import load_dotenv
from os import environ
load_dotenv('.env')

REDIS_TOPIC = 'block_hq'

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
handler = logging.FileHandler("logs/sockets.log")
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

app = Flask(__name__)
app.debug = 'DEBUG' in os.environ

sockets = Sockets(app)
redis = redis.from_url("redis://%s:6379" % environ.get("redis_host_local"))

class ChatBackend(object):
    clients = {}

    def __init__(self):
        self.pubsub = redis.pubsub()
        self.pubsub.subscribe(REDIS_TOPIC)

    def __iter_data(self):
        for message in self.pubsub.listen():
            data = message.get('data')
            if message['type'] == 'message':
                yield data

    def register(self, code, client):
        print code, "register"
        if code not in self.clients:
            self.clients[code] = set()

        self.clients[code].add(client)

    def send(self, client, data):
        try:
            data = data.decode("utf-8")
            client.send(data)
        except Exception, e:
            print e
            # self.clients.discard(client)

    def run(self):
        try:
            for data in self.__iter_data():
                if "href" in data:
                    continue
                data_json = json.loads(data)
                try:
                    code = data_json[0]
                    if code in self.clients:
                        for client in self.clients[code]:
                            gevent.spawn(self.send, client, data)

                except Exception, e:
                    logger.error(e.message)
                    continue

        except Exception, e:
            logger.error(e.message)

    def start(self):
        gevent.spawn(self.run)

@sockets.route('/close')
def close(ws):
    print "close"

@sockets.route('/receive')
def outbox(ws):
    while not ws.closed:
        message = str(ws.receive())
        print message
        if message.startswith("subscribe:"):
            code = message.split(":")[-1].split(",")
            for c in code:
                chats.register(c, ws)

        gevent.sleep(0.1)

chats = ChatBackend()
chats.start()
