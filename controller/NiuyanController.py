# -*- coding: utf-8 -*-
from Controller import Controller
import json, redis, time
from settings import redis_config
from model.crawl_block_finance import CrawlBlockFinance

class NiuyanController(Controller):
    def __init__(self, topic="niuyan_hangqing"):
        super(NiuyanController, self).__init__(topic, 'niuyan_hangqing')
        self.r = redis.Redis(host=redis_config['host'], port=redis_config['port'])
        self.code_price = {}

    def run(self):
        for msg in self.consumer:
            try:
                data = json.loads(msg.value.decode('utf-8'))
                code = data[0]
                price = data[1]
                now = time.time()

                # print code, price, now
                if code in self.code_price:
                    last_update = self.code_price[code]['last_update']
                    # print code, last_update
                    if now - last_update > 2:
                        coin = CrawlBlockFinance(coin_id=code, price=price)
                        with self.session_scope(self.sess) as session:
                            query = session.query(CrawlBlockFinance.id).filter(
                                CrawlBlockFinance.coin_id == coin.coin_id
                            ).one_or_none()

                            # print "add coin %s " % code
                            if query is None:
                                session.add(coin)
                            else:
                                session.query(CrawlBlockFinance).filter(
                                    CrawlBlockFinance.id == query[0]
                                ).update({'price': price})

                else:
                    self.code_price[code] = {
                        'last_update': time.time()
                    }

                    # print self.code_price

                self.r.publish("block_hq", msg.value.decode('utf-8'))
            except:
                self.logger.error('Catch an exception.', exc_info=True)
