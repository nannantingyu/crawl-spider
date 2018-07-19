# -*- coding: utf-8 -*-
from model.crawl_forex_exchange_soft import CrawlForexExchangeSoft
from Controller import Controller
import json, re, requests, logging
from sqlalchemy import and_, or_, func

class ForeignexchangesoftController(Controller):
    def __init__(self, topic="crawl_foreign_exchange_soft"):
        super(ForeignexchangesoftController, self).__init__(topic, 'foreign_exchange_soft')

    def run(self):
        for msg in self.consumer:
            data = json.loads(msg.value.decode('utf-8'))

            with self.session_scope(self.sess) as session:
                try:
                    print data
                    crawlForexExchangeSoft = CrawlForexExchangeSoft(**data)
                    query = session.query(CrawlForexExchangeSoft.id).filter(
                        and_(
                            CrawlForexExchangeSoft.fid == crawlForexExchangeSoft.fid,
                            CrawlForexExchangeSoft.soft_type == crawlForexExchangeSoft.soft_type
                        )
                    ).one_or_none()

                    if query is None:
                        session.add(crawlForexExchangeSoft)
                        session.flush()
                    else:
                        session.query(CrawlForexExchangeSoft)\
                            .filter(CrawlForexExchangeSoft.id == query[0])\
                            .update(data)
                except Exception,e:
                    session.rollback()
                    self.logger.error('Catch an exception.', exc_info=True)