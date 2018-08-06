# -*- coding: utf-8 -*-
from model.crawl_article import CrawlArticle
from model.crawl_article_body import CrawlArticleBody
from model.crawl_category import CrawlCategory
from model.crawl_article_category import CrawlArticleCategory
from Controller import Controller
from model.crawl_category_map import CrawlCategoryMap
import json, logging, time, hashlib

class ArticleController(Controller):
    def __init__(self, topic="crawl_article"):
        super(ArticleController, self).__init__(topic, 'article')
        self.category_map = {}
        self.category_start_time = None

    def md5(self, str):
        try:
            str = str.encode('utf-8')
        except:
            self.logger.error('cannot encode '+ str)

        return hashlib.md5(str).hexdigest()

    def get_category_map(self):
        time_now = time.time()
        # 设置过期时间
        if self.category_start_time is None or time_now - self.category_start_time > 300:
            with self.session_scope(self.sess) as session:
                try:
                    maps = session.query(CrawlCategoryMap).all()
                    for map in maps:
                        map_key = self.md5("%s-%s" % (map.source_site, map.source_category))
                        if map_key in self.category_map:
                            self.category_map[map_key].append(map.target)
                        else:
                            self.category_map[map_key] = [map.target]

                    self.category_start_time = time.time()
                except Exception,e:
                    print e
                    session.rollback()
                    return None

        return self.category_map

    def run(self):
        category_map = self.get_category_map()
        for msg in self.consumer:
            try:
                data = json.loads(msg.value.decode('utf-8'))
                if 'dtype' in data:
                    del data['dtype']

                if "key" in data:
                    del data['key']

                print data
                body = None
                if 'body' in data:
                    body = data['body']
                    del data['body']

                article = CrawlArticle(**data)
                with self.session_scope(self.sess) as session:
                    query = session.query(CrawlArticle, CrawlArticleBody.body)\
                        .outerjoin(CrawlArticleBody, CrawlArticle.id == CrawlArticleBody.aid)\
                        .filter(CrawlArticle.source_id == article.source_id).one_or_none()

                    if query is None:
                        session.add(article)
                        session.flush()
                    else:
                        article = query[0]
                        session.query(CrawlArticle).filter(CrawlArticle.source_id == article.source_id).update(data)

                    if body is not None:
                        if query is None or query[1] is None:
                            session.add(CrawlArticleBody(aid=article.id, body=body))
                        elif query[1] is not None:
                            session.query(CrawlArticleBody).filter(CrawlArticleBody.aid == article.id).update({"body":body})

                    if body:
                        self.hook_data('read/%s' % article.id)
                        self.logger.info('Notify generate article info http://www.jujin8.com/read/%s' % article.id)

                    # 触发生成静态文件
                    category_map = self.get_category_map()
                    if category_map is not None:
                        pass

                    map_key = self.md5("%s-%s" % (article.source_site, article.type))
                    if map_key in self.category_map:
                        category_ids = self.category_map[map_key]
                        category = session.query(CrawlCategory).filter(
                            CrawlCategory.id.in_(category_ids)
                        ).all()
                    else:
                        category = session.query(CrawlCategory).filter(
                            CrawlCategory.name == article.type
                        ).all()

                    if category is not None:
                        if body:
                            for ca in category:
                                self.hook_data('news/%s' % ca.ename)
                                self.logger.info('Notify generate article list http://www.jujin8.com/news/%s' % ca.ename)

                                # 添加文章分类
                                articleCategory = CrawlArticleCategory(aid=article.id, cid=ca.id);
                                session.add(articleCategory)
            except Exception as e:
                self.logger.error('Catch an exception.', exc_info=True)