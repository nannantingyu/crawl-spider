# -*- coding: utf-8 -*-
from model.crawl_forex_exchange import CrawlForexExchange
from Controller import Controller
import json, re, requests, logging
from sqlalchemy import and_, or_, func

class ForeignexchangeController(Controller):
    def __init__(self, topic="crawl_foreign_exchange"):
        super(ForeignexchangeController, self).__init__(topic, 'foreign_exchange')

    def run(self):
        for msg in self.consumer:
            data = json.loads(msg.value.decode('utf-8'))

            with self.session_scope(self.sess) as session:
                try:
                    if 'companyNameStr' in data: del data['companyNameStr']
                    crawlForexExchange = CrawlForexExchange(**data)
                    query = session.query(CrawlForexExchange.id).filter(
                        and_(
                            CrawlForexExchange.source_id == crawlForexExchange.source_id
                        )
                    ).one_or_none()

                    if query is None:
                        session.add(crawlForexExchange)
                        session.flush()
                    else:
                        session.query(CrawlForexExchange)\
                            .filter(CrawlForexExchange.id == query[0])\
                            .update(data)
                except Exception,e:
                    session.rollback()
                    self.logger.error('Catch an exception.', exc_info=True)