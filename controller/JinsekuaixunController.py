# -*- coding: utf-8 -*-
from model.crawl_jinse_kuaixun import CrawlJinseKuaixun
from Controller import Controller
import json, re, requests, logging, datetime, time
from sqlalchemy import and_, or_, func

class JinsekuaixunController(Controller):
    def __init__(self, topic="crawl_jinse_kuaixun"):
        super(JinsekuaixunController, self).__init__(topic, 'jinse_kuaixun')
        self.key_map = {
            'live_id': 'source_id',
            'content': 'body',
            'source': 'source_site',
            'grade': 'importance'
        }

        self.delete_keys = ['website', 'topic_id']

    def run(self):
        for msg in self.consumer:
            try:
                data = json.loads(msg.value.decode('utf-8'))
                data = self.delete_key(data)
                data = self.key_replace(data)

                jinseKuaixun = CrawlJinseKuaixun(**data)
                with self.session_scope(self.sess) as session:
                    try:
                        query = session.query(CrawlJinseKuaixun.id).filter(and_(
                            CrawlJinseKuaixun.source_id == data['source_id']
                        )).one_or_none()

                        if query is None:
                            session.add(jinseKuaixun)
                            session.flush()
                        else:
                            session.query(CrawlJinseKuaixun)\
                                .filter(CrawlJinseKuaixun.source_id == data['source_id'])\
                                .update(data)
                    except Exception,e:
                        session.rollback()
            except:
                self.logger.error('Catch an exception.', exc_info=True)
                continue