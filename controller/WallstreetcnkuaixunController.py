# -*- coding: utf-8 -*-
from model.crawl_article import CrawlArticle
from model.crawl_wallstreetcn_kuaixun import CrawlWallstreetcnKuaixun
from Controller import Controller
import json, requests, re, logging

class WallstreetcnkuaixunController(Controller):
    def __init__(self, topic="crawl_wallstreetcn_kuaixun"):
        super(WallstreetcnkuaixunController, self).__init__(topic, 'wallstreetcn_kuaixun')

    def run(self):
        for msg in self.consumer:
            try:
                data = json.loads(msg.value.decode('utf-8'))
                del data['dtype']

                kuaixun = CrawlWallstreetcnKuaixun(**data)
                with self.session_scope(self.sess) as session:
                    query = session.query(CrawlWallstreetcnKuaixun.id).filter(
                        CrawlWallstreetcnKuaixun.dateid == kuaixun.dateid
                    ).one_or_none()

                    print query
                    if query is None:
                        session.add(kuaixun)
                        session.flush()
                        data['id'] = kuaixun.id
                        data['dtype'] = "insert"
                        data['source_site'] = 'wallstreetcn'
                        self.hook_data(data, "kuaixun")
                    else:
                        session.query(CrawlWallstreetcnKuaixun).filter(
                            CrawlWallstreetcnKuaixun.id == query[0]
                        ).update(data)

                        data['id'] = query[0]
                        data['dtype'] = "update"
                        data['source_site'] = 'wallstreetcn'
                        self.hook_data(data, "kuaixun")
            except Exception, e:
                self.logger.error('Catch an exception.', exc_info=True)