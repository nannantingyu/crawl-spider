# -*- coding: utf-8 -*-
from model.crawl_article import CrawlArticle
from model.crawl_economic_jiedu import CrawlEconomicJiedu
from Controller import Controller
import json

class Jin10jieduController(Controller):
    def __init__(self, topic="crawl_jin10_calendar_jiedu"):
        super(Jin10jieduController, self).__init__(topic, 'jin10_calendar_jiedu')

    def run(self):
        for msg in self.consumer:
            data = json.loads(msg.value.decode('utf-8'))

            with self.session_scope(self.sess) as session:
                try:
                    jiedu = CrawlEconomicJiedu(**data)
                    query = session.query(CrawlEconomicJiedu.dataname_id).filter(
                        CrawlEconomicJiedu.dataname_id == jiedu.dataname_id
                    ).one_or_none()

                    if query is None:
                        session.add(jiedu)
                        session.flush()
                    else:
                        session.query(CrawlEconomicJiedu).filter(
                            CrawlEconomicJiedu.dataname_id == query[0]
                        ).update(data)
                except:
                    session.rollback()
                    self.logger.error('Catch an exception.', exc_info=True)