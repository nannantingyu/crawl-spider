# -*- coding: utf-8 -*-
from model.crawl_cftc import CrawlCftc
from kafka import KafkaConsumer
from Controller import Controller
import json, re, requests, logging
from sqlalchemy import and_, or_, func

class CftcController(Controller):
    def __init__(self, topic="crawl_cftc_new"):
        super(CftcController, self).__init__(topic, 'cftc')

    def run(self):
        for msg in self.consumer:
            data = json.loads(msg.value.decode('utf-8'))
            cftc = CrawlCftc(**data)
            with self.session_scope(self.sess) as session:
                try:
                    query = session.query(CrawlCftc.id).filter(
                        and_(
                            CrawlCftc.cftc_name == cftc.cftc_name,
                            CrawlCftc.publish_time == cftc.publish_time,
                            CrawlCftc.publish_time_end == cftc.publish_time_end,
                        )
                    ).one_or_none()

                    if query is None:
                        session.add(cftc)
                        session.flush()
                    else:
                        session.query(CrawlCftc).filter(CrawlCftc.id == query[0]).update({
                            "net_long": cftc.net_long,
                            "net_short": cftc.net_short
                        })
                except Exception,e:
                    session.rollback()
                    self.logger.error('Catch an exception.', exc_info=True)