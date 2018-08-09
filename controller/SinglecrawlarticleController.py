# -*- coding: utf-8 -*-
from model.crawl_article import CrawlArticle
from model.crawl_article_body import CrawlArticleBody
from model.crawl_category import CrawlCategory
from model.crawl_article_category import CrawlArticleCategory
from Controller import Controller
from model.crawl_crawl_article import CrawlCrawlArticle
import json, logging, time, hashlib
from sqlalchemy import and_, or_, func

class SinglecrawlarticleController(Controller):
    def __init__(self, topic="single_crawl_article"):
        super(SinglecrawlarticleController, self).__init__(topic, 'single_crawl_article')
        self.category_map = {}
        self.category_start_time = None

    def md5(self, str):
        try:
            str = str.encode('utf-8')
        except:
            self.logger.error('cannot encode '+ str)

        return hashlib.md5(str).hexdigest()

    def get_category_by_url(self, url, session):
        category = None

        try:
            category = session.query(CrawlCrawlArticle.categories).filter(
                CrawlCrawlArticle.url == url
            ).one_or_none()

            if category is not None:
                category = session.query(CrawlCategory).filter(
                    CrawlCategory.id.in_(str(category[0]).split(','))
                ).all()

        except Exception as e:
            self.logger.error('Catch an exception.', exc_info=True)
        finally:
            return category


    def run(self):
        for msg in self.consumer:
            try:
                data = json.loads(msg.value.decode('utf-8'))
                if 'dtype' in data:
                    del data['dtype']

                if "key" in data:
                    del data['key']

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

                    category = self.get_category_by_url(article.source_url, session)
                    if category is not None:
                        if body:
                            for ca in category:
                                self.hook_data('news/%s' % ca.ename)
                                self.logger.info('Notify generate article list http://www.jujin8.com/news/%s' % ca.ename)

                                # 添加文章分类
                                query_type = session.query(CrawlArticleCategory).filter(and_(
                                    CrawlArticleCategory.aid == article.id,
                                    CrawlArticleCategory.cid == ca.id
                                )).one_or_none()

                                print article.id, ca.id
                                if query_type is None:
                                    articleCategory = CrawlArticleCategory(aid=article.id, cid=ca.id);
                                    session.add(articleCategory)
            except Exception as e:
                self.logger.error('Catch an exception.', exc_info=True)