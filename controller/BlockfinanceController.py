# -*- coding: utf-8 -*-
from model.crawl_block_finance import CrawlBlockFinance
from Controller import Controller
import json, re, requests, logging, datetime, time
from sqlalchemy import and_, or_, func

class BlockfinanceController(Controller):
    def __init__(self, topic="crawl_block_finance"):
        super(BlockfinanceController, self).__init__(topic, 'block_finance')

    def run(self):
        for msg in self.consumer:
            try:
                data = json.loads(msg.value.decode('utf-8'))
                print data

                with self.session_scope(self.sess) as session:
                    try:
                        for coin in data:
                            print data[coin]
                            coin_finance = CrawlBlockFinance(coin_id=coin, price=data[coin])
                            query = session.query(CrawlBlockFinance.id).filter(
                                and_(
                                    CrawlBlockFinance.coin_id == coin_finance.coin_id,
                                )
                            ).one_or_none()

                            if query is None:
                                session.add(coin_finance)
                                session.flush()
                            else:
                                session.query(CrawlBlockFinance).filter(
                                    CrawlBlockFinance.id == query[0]
                                ).update(coin)
                    except Exception, e:
                        session.rollback()
                        self.logger.error('Catch an exception.', exc_info=True)
            except:
                self.logger.error('Catch an exception.', exc_info=True)
                continue