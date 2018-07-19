# -*- coding: utf-8 -*-
from model.crawl_article import CrawlArticle
from model.crawl_fx678_kuaixun import CrawlFx678Kuaixun
from Controller import Controller
import json, requests, re, logging

class Fx678kuaixunController(Controller):
    def __init__(self, topic="crawl_fx678_kuaixun"):
        super(Fx678kuaixunController, self).__init__(topic, 'fx678_kuaixun.log')

        self.post_data = {
            'category': '市场数据',
            'title': '',
            'content': '',
            'keyname': '',
            'description': '',
            'name': '',
            'status': 1,
            'link_id': '',
            'vip': '',
            'tpl': 1,
            'todo': 0,
            'flag': '',
            'var1': '',
            'var2': '',
            'var3': '',
            'pk1': '',
            'star': '',
            'token': self.token
        }

    def run(self):
        for msg in self.consumer:
            try:
                data = json.loads(msg.value.decode('utf-8'))
                dtype = data['dtype']
                del data['dtype']

                kuaixun = CrawlFx678Kuaixun(**data)
                if 'fx678' in kuaixun.body or 'fx678' in kuaixun.body or 'fx678' in kuaixun.more_link:
                    continue

                post_data = self.get_post_data(data)
                with self.session_scope(self.sess) as session:
                    if dtype == 'insert':
                        session.add(kuaixun)
                        result = requests.post(self.post_sn_url, post_data)
                        print "insert", result.content
                        res = result.json()
                        if 'errno' in res and res['errno'] == 0:
                            session.query(CrawlFx678Kuaixun).filter(
                                CrawlFx678Kuaixun.dateid == kuaixun.dateid
                            ).update({'fx_id': res['data']['id']})
                    elif dtype == 'update':
                        query = session.query(CrawlFx678Kuaixun.id, CrawlFx678Kuaixun.fx_id).filter(
                            CrawlFx678Kuaixun.dateid == kuaixun.dateid
                        ).one_or_none()
                        if query:
                            post_data['id'] = query[1]
                            result = requests.post(self.post_sn_url, post_data)
                            session.query(CrawlFx678Kuaixun).filter(
                                CrawlFx678Kuaixun.id == query[0]
                            ).update(data)
                    elif dtype == 'delete':
                        print "delete"
                        session.query(CrawlFx678Kuaixun).filter(
                            CrawlFx678Kuaixun.dateid == kuaixun.dateid
                        ).delete()
            except Exception, e:
                logging.error(e)

    def get_post_data(self, data):
        key_map = {
            'former_value': 'var1',
            'predicted_value': 'var2',
            'published_value': 'var3',
            'more_link': 'link_id',
            'star': 'star',
            'importance': 'vip',
            'body': 'content',
            'publish_time': 'show_time',
            'dateid': 'crawl_id',
            'image': 'cover',
            'country': 'flag',
            'influence': 'pk1'
        }

        post_data = {}
        post_data.update(self.post_data)

        time_pat = re.compile(r"\d{4}\-\d{2}\-\d{2}(\s\d{2}:\d{2}:\d{2})?")
        for d in data:
            if d in key_map:
                post_data[key_map[d]] = data[d]

        if 'show_time' in post_data and len(time_pat.findall(post_data['show_time'])) == 0:
            post_data['show_time'] = None

        if 'vip' in post_data:
            try:
                post_data['vip'] = 1 - int(post_data['vip'])
            except ValueError,e:
                post_data['vip'] = 0

        return post_data