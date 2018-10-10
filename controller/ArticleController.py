# -*- coding: utf-8 -*-
from model.crawl_article import CrawlArticle
from model.crawl_article_body import CrawlArticleBody
from model.crawl_category import CrawlCategory
from model.crawl_article_category import CrawlArticleCategory
from Controller import Controller
from model.crawl_category_map import CrawlCategoryMap
from model.crawl_config import CrawlConfig
import json, logging, time, hashlib
from sqlalchemy import and_, or_, func

class ArticleController(Controller):
    def __init__(self, topic="crawl_article"):
        super(ArticleController, self).__init__(topic, 'article')
        self.category_map = {}
        self.category_start_time = None

        self.source_site_state = {}
        self.source_site_start_time = None

    def md5(self, str):
        try:
            str = str.encode('utf-8')
        except:
            self.logger.error('cannot encode '+ str)

        return hashlib.md5(str).hexdigest()

    def get_source_site_state(self):
        time_now = time.time()
        # 设置过期时间
        if self.source_site_start_time is None or time_now - self.source_site_start_time > 300:
            with self.session_scope(self.sess) as session:
                try:
                    config = session.query(CrawlConfig).filter(CrawlConfig.key == 'article_source_site').one_or_none()

                    if config:
                        config_value = json.loads(config.value)
                        for c in config_value:
                            self.source_site_state[c['site']] = c['state']

                    self.source_site_start_time = time.time()
                except Exception,e:
                    print e
                    session.rollback()
                    return None

        return self.source_site_state

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
        for msg in self.consumer:
            try:
                data = json.loads(msg.value.decode('utf-8'))
                if 'dtype' in data:
                    del data['dtype']

                if "key" in data:
                    del data['key']

                # print data
                body = None
                if 'body' in data:
                    body = data['body']
                    del data['body']

                article = CrawlArticle(**data)
                with self.session_scope(self.sess) as session:
                    query = session.query(CrawlArticle, CrawlArticleBody.body)\
                        .outerjoin(CrawlArticleBody, CrawlArticle.id == CrawlArticleBody.aid)\
                        .filter(or_(
                            CrawlArticle.source_id == article.source_id,
                            and_(CrawlArticle.title == article.title, CrawlArticle.publish_time == article.publish_time)
                        )).one_or_none()

                    if query is None:
                        session.add(article)
                        session.flush()
                    else:
                        article = query[0]
                        session.query(CrawlArticle).filter(CrawlArticle.source_id == article.source_id).update(data)

                    # 如果设置来源网站不发布，则将新文章的状态设置为0
                    source_site_state = self.get_source_site_state()
                    if article.source_site in source_site_state:
                        article.state = source_site_state[article.source_site]

                    print article.state
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

                    all_categories = []
                    for type in str(article.type).split(','):
                        type = unicode(type, 'utf-8')
                        map_key = self.md5("%s-%s" % (article.source_site, type))
                        if map_key in self.category_map:
                            category_ids = self.category_map[map_key]
                            category = session.query(CrawlCategory).filter(
                                CrawlCategory.id.in_(category_ids)
                            ).all()
                        else:
                            category = session.query(CrawlCategory).filter(
                                CrawlCategory.name == type
                            ).all()

                        if category:
                            all_categories += category

                    if len(all_categories) > 0:
                        if body:
                            for ca in all_categories:
                                print ca.ename
                                self.hook_data('news/%s' % ca.ename)
                                self.logger.info('Notify generate article list http://www.jujin8.com/news/%s' % ca.ename)

                                # 添加文章分类
                                query_type = session.query(CrawlArticleCategory).filter(and_(
                                    CrawlArticleCategory.aid == article.id,
                                    CrawlArticleCategory.cid == ca.id
                                )).one_or_none()

                                if query_type is None:
                                    articleCategory = CrawlArticleCategory(aid=article.id, cid=ca.id)
                                    session.add(articleCategory)
            except Exception as e:
                self.logger.error('Catch an exception.', exc_info=True)