# -*- coding: utf-8 -*-
from model.crawl_block_info import CrawlBlockInfo
from Controller import Controller
import json, re, requests, logging, datetime, time
from sqlalchemy import and_, or_, func

class BlockinfoController(Controller):
    def __init__(self, topic="crawl_block_info"):
        super(BlockinfoController, self).__init__(topic, 'block_info')

    def run(self):
        for msg in self.consumer:
            try:
                data = json.loads(msg.value.decode('utf-8'))
                blockInfo = CrawlBlockInfo(**data)
                print blockInfo

                with self.session_scope(self.sess) as session:
                    try:
                        query = session.query(CrawlBlockInfo.id).filter(
                            and_(
                                CrawlBlockInfo.coin_id == blockInfo.coin_id,
                            )
                        ).one_or_none()

                        if query is None:
                            session.add(blockInfo)
                            session.flush()
                        else:
                            session.query(CrawlBlockInfo).filter(
                                CrawlBlockInfo.id == query[0]
                            ).update(data)
                    except Exception, e:
                        session.rollback()
                        self.logger.error('Catch an exception.', exc_info=True)
            except:
                self.logger.error('Catch an exception.', exc_info=True)
                continue