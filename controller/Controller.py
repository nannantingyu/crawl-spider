# -*- coding: utf-8 -*-
import sys, os, logging, datetime
reload(sys)
sys.setdefaultencoding("utf-8")
from kafka import KafkaConsumer
from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker
from model.util import db_connect, create_news_table
import settings
from pykafka import KafkaClient

@contextmanager
def session_scope(session):
    sess = session()
    try:
        yield sess
        sess.commit()
    except:
        sess.rollback()
        raise
    finally:
        sess.close()

class Controller(object):
    def __init__(self, topic, name):
        engine = db_connect()
        create_news_table(engine)
        self.sess = sessionmaker(bind=engine)
        self.server = settings.kafka
        self.session_scope = session_scope
        self.token = '9286168e06a110cd374caa0f67f08199'
        self.name = name

        log_dir = os.path.join("logs", datetime.datetime.now().strftime("%Y%m%d"))
        if not os.path.exists(log_dir):
            os.mkdir(log_dir)

        self.logger = logging.getLogger()
        handler = logging.FileHandler(filename=os.path.join(log_dir, "%s.log"%name))
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.ERROR)

        print self.server
        self.client = KafkaClient(hosts=self.server['host'])
        self.producers = {}

        if topic:
            self.consumer = KafkaConsumer(topic, bootstrap_servers=self.server['host'], group_id='cms_consumer_client')

    def __del__(self) :
        if hasattr(self, "producers"):
            for p in self.producers:
                del p

    # 替换kafka中获取的data的键
    def key_replace(self, data):
        for key in self.key_map:
            if key in data:
                data[self.key_map[key]] = data[key]
                del data[key]

        return data

    # 删除kafka中获取的data的键
    def delete_key(self, data):
        for key in self.delete_keys:
            if key in data:
                del data[key]

        return data

    def hook_data(self, url, topic_name='jujin8_template'):
        if topic_name in self.producers:
            p = self.producers[topic_name]
        else:
            topic = self.client.topics[topic_name]
            p = topic.get_sync_producer()
            self.producers[topic_name] = p

        p.produce(bytes(url))