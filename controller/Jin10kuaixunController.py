# -*- coding: utf-8 -*-
from model.crawl_jin10_kuaixun import CrawlJin10Kuaixun
from Controller import Controller
import json, requests, re, logging

class Jin10kuaixunController(Controller):
    def __init__(self, topic="crawl_jin10_kuaixun"):
        super(Jin10kuaixunController, self).__init__(topic, 'jin10_kuaixun')
        self.key_map = {
            'dateid': 'source_id'
        }

        self.delete_keys = [ 't0', 't5', 't7', 't8', 't10', 't12', 'dtype', 'key', 'real_time', 'calendar_id', 'fx_id', 'time_detail', 'updated_time', 'created_time' ]

    def run(self):
        for msg in self.consumer:
            try:
                print msg
                data = json.loads(msg.value.decode('utf-8'))
                key = data['key']
                if key in self.key_map: key = self.key_map[key]

                data = self.delete_key(data)
                data = self.key_replace(data)

                kuaixun = CrawlJin10Kuaixun(**data)
                if (kuaixun.body and ('金十' in kuaixun.body or 'jin10' in kuaixun.body)) or (kuaixun.more_link and 'jin10' in kuaixun.more_link):
                    continue

                with self.session_scope(self.sess) as session:
                    try:
                        query = session.query(CrawlJin10Kuaixun.id).filter(
                            getattr(CrawlJin10Kuaixun, key) == getattr(kuaixun, key)
                        ).one_or_none()

                        if query is None:
                            session.add(kuaixun)
                            session.flush()
                        else:
                            session.query(CrawlJin10Kuaixun).filter(
                                CrawlJin10Kuaixun.id == query[0]
                            ).update(data)
                    except Exception,e:
                        session.rollback()

            except Exception, e:
                self.logger.error('Catch an exception.', exc_info=True)