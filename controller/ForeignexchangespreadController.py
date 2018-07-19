# -*- coding: utf-8 -*-
from model.crawl_forex_exchange_spread import CrawlForexExchangeSpread
from Controller import Controller
import json, re, requests, logging
from sqlalchemy import and_, or_, func

class ForeignexchangespreadController(Controller):
    def __init__(self, topic="crawl_foreign_exchange_spread"):
        super(ForeignexchangespreadController, self).__init__(topic, 'foreign_exchange_spread')

    def run(self):
        for msg in self.consumer:
            data = json.loads(msg.value.decode('utf-8'))

            with self.session_scope(self.sess) as session:
                try:
                    print data
                    crawlForexExchangeSpread = CrawlForexExchangeSpread(**data)
                    query = session.query(CrawlForexExchangeSpread.id).filter(
                        and_(
                            CrawlForexExchangeSpread.fid == crawlForexExchangeSpread.fid,
                            CrawlForexExchangeSpread.symble == crawlForexExchangeSpread.symble
                        )
                    ).one_or_none()

                    if query is None:
                        session.add(crawlForexExchangeSpread)
                        session.flush()
                    else:
                        session.query(CrawlForexExchangeSpread)\
                            .filter(CrawlForexExchangeSpread.id == query[0])\
                            .update(data)
                except Exception,e:
                    session.rollback()
                    self.logger.error('Catch an exception.', exc_info=True)