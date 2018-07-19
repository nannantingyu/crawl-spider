# -*- coding: utf-8 -*-
from model.crawl_forex_exchange_withdraw import CrawlForexExchangeWithdraw
from Controller import Controller
import json, re, requests, logging
from sqlalchemy import and_, or_, func

class ForeignexchangewithdrawController(Controller):
    def __init__(self, topic="crawl_foreign_exchange_withdraw"):
        super(ForeignexchangewithdrawController, self).__init__(topic, 'foreign_exchange_withdraw')

    def run(self):
        for msg in self.consumer:
            data = json.loads(msg.value.decode('utf-8'))

            with self.session_scope(self.sess) as session:
                try:
                    print data
                    crawlForexExchangeWithdraw = CrawlForexExchangeWithdraw(**data)
                    query = session.query(CrawlForexExchangeWithdraw.id).filter(
                        and_(
                            CrawlForexExchangeWithdraw.fid == crawlForexExchangeWithdraw.fid,
                            CrawlForexExchangeWithdraw.withdraw_way == crawlForexExchangeWithdraw.withdraw_way
                        )
                    ).one_or_none()

                    if query is None:
                        session.add(crawlForexExchangeWithdraw)
                        session.flush()
                    else:
                        session.query(CrawlForexExchangeWithdraw)\
                            .filter(CrawlForexExchangeWithdraw.id == query[0])\
                            .update(data)
                except Exception,e:
                    session.rollback()
                    self.logger.error('Catch an exception.', exc_info=True)