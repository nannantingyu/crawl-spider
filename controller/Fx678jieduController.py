# -*- coding: utf-8 -*-
from model.crawl_article import CrawlArticle
from model.crawl_fx678_economic_jiedu import CrawlFx678EconomicJiedu
from Controller import Controller
import json, requests, re, logging

class Fx678jieduController(Controller):
    def __init__(self, topic="crawl_fx678_calendar_jiedu"):
        super(Fx678jieduController, self).__init__(topic, 'fx678_jiedu.log')

    def run(self):
        for msg in self.consumer:
            data = json.loads(msg.value.decode('utf-8'))

            with self.session_scope(self.sess) as session:
                try:
                    jiedu = CrawlFx678EconomicJiedu(**data)
                    query = session.query(CrawlFx678EconomicJiedu.dataname_id).filter(
                        CrawlFx678EconomicJiedu.dataname_id == jiedu.dataname_id
                    ).one_or_none()

                    if query is None:
                        session.add(jiedu)
                        session.flush()
                        data['id'] = jiedu.id
                        data['dtype'] = "insert"
                        data['source_site'] = "fx678"
                        self.hook_data(data, "jiedu")
                    else:
                        session.query(CrawlFx678EconomicJiedu).filter(
                            CrawlFx678EconomicJiedu.dataname_id == query[0]
                        ).update(data)

                        data['id'] = jiedu.id
                        data['dtype'] = "update"
                        data['source_site'] = "fx678"
                        self.hook_data(data, "jiedu")
                except:
                    self.logger.error('Catch an exception.', exc_info=True)