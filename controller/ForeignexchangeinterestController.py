# -*- coding: utf-8 -*-
from model.crawl_forex_exchange_interest import CrawlForexExchangeInterest
from Controller import Controller
import json, re, requests, logging
from sqlalchemy import and_, or_, func

class ForeignexchangeinterestController(Controller):
    def __init__(self, topic="crawl_foreign_exchange_interest"):
        super(ForeignexchangeinterestController, self).__init__(topic, 'foreign_exchange_interest')

    def run(self):
        for msg in self.consumer:
            data = json.loads(msg.value.decode('utf-8'))

            with self.session_scope(self.sess) as session:
                try:
                    print data
                    crawlForexExchangeInterest = CrawlForexExchangeInterest(**data)
                    query = session.query(CrawlForexExchangeInterest.id).filter(
                        and_(
                            CrawlForexExchangeInterest.fid == crawlForexExchangeInterest.fid,
                            CrawlForexExchangeInterest.symble == crawlForexExchangeInterest.symble
                        )
                    ).one_or_none()

                    if query is None:
                        session.add(crawlForexExchangeInterest)
                        session.flush()
                    else:
                        session.query(CrawlForexExchangeInterest)\
                            .filter(CrawlForexExchangeInterest.id == query[0])\
                            .update(data)
                except Exception,e:
                    session.rollback()
                    self.logger.error('Catch an exception.', exc_info=True)