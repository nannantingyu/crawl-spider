# -*- coding: utf-8 -*-
from model.crawl_fxssi import CrawlFxssi
from Controller import Controller
import json, re, requests, logging, datetime, time
from sqlalchemy import and_, or_, func

class FxssiController(Controller):
    def __init__(self, topic="crawl_fxssi"):
        super(FxssiController, self).__init__(topic, 'fxssi')

    def run(self):
        for msg in self.consumer:
            try:
                datas = json.loads(msg.value.decode('utf-8'))
                time = datas['day']
                data = datas['data']
                with self.session_scope(self.sess) as session:
                    session.query(CrawlFxssi).filter(and_(
                        CrawlFxssi.day == time
                    )).delete()

                    all_data = []
                    for pair in data:
                        for broker in data[pair]:
                                fxssi = CrawlFxssi()
                                fxssi.broker = broker
                                fxssi.pair = pair
                                fxssi.day = time
                                fxssi.val = data[pair][broker] if self.is_float(data[pair][broker]) else 50

                                all_data.append(fxssi)
                    if all_data:
                        session.add_all(all_data)
            except:
                self.logger.error('Catch an exception.', exc_info=True)
                continue

    def is_float(self, num):
        if num == 'NaN':
            return False
        try:
            float(num)
            return True
        except:
            return False
