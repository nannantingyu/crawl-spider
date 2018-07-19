# -*- coding: utf-8 -*-
from model.crawl_forex_exchange_account import CrawlForexExchangeAccount
from Controller import Controller
import json, re, requests, logging
from sqlalchemy import and_, or_, func

class ForeignexchangeaccountController(Controller):
    def __init__(self, topic="crawl_foreign_exchange_account"):
        super(ForeignexchangeaccountController, self).__init__(topic, 'foreign_exchange_account')

    def run(self):
        for msg in self.consumer:
            data = json.loads(msg.value.decode('utf-8'))

            with self.session_scope(self.sess) as session:
                try:
                    data['lock_position'] = 1 if data['lock_position'] == '允许' else 0
                    data['scalp'] = 1 if data['scalp'] == '允许' else 0
                    data['ea'] = 1 if data['lock_position'] == '支持' else 0
                    data['biggest_leverage'] = data['biggest_leverage'].split(':')[-1]
                    data['explosion'] = data['explosion'].split('%')[0]
                    data['explosion'] = data['explosion'] if data['explosion'] else 0

                    crawlForexExchangeAccount = CrawlForexExchangeAccount(**data)
                    query = session.query(CrawlForexExchangeAccount.id).filter(
                        and_(
                            CrawlForexExchangeAccount.fid == crawlForexExchangeAccount.fid,
                            CrawlForexExchangeAccount.account_type == crawlForexExchangeAccount.account_type
                        )
                    ).one_or_none()

                    if query is None:
                        session.add(crawlForexExchangeAccount)
                        session.flush()
                    else:
                        session.query(CrawlForexExchangeAccount)\
                            .filter(CrawlForexExchangeAccount.id == query[0])\
                            .update(data)
                except Exception,e:
                    session.rollback()
                    self.logger.error('Catch an exception.', exc_info=True)