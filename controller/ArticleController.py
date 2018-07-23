# -*- coding: utf-8 -*-
from model.crawl_article import CrawlArticle
from model.crawl_article_body import CrawlArticleBody
from model.crawl_category import CrawlCategory
from model.crawl_article_category import CrawlArticleCategory
from Controller import Controller
import json, logging, time

class ArticleController(Controller):
    def __init__(self, topic="crawl_article"):
        super(ArticleController, self).__init__(topic, 'article')

    def run(self):
        for msg in self.consumer:
            try:
                data = json.loads(msg.value.decode('utf-8'))
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

                    if body:
                        self.hook_data('read/%s' % article.id)
                        self.logger.info('Notify generate article info http://www.jujin8.com/read/%s' % article.id)

                    # 触发生成静态文件
                    category = session.query(CrawlCategory).filter(
                        CrawlCategory.name == article.type
                    ).one_or_none()

                    if category is not None:
                        if body:
                            self.hook_data('news/%s' % category.ename)
                            self.logger.info('Notify generate article list http://www.jujin8.com/news/%s' % category.ename)

                        # 添加文章分类
                        articleCategory = CrawlArticleCategory(aid=article.id, cid=category.id);
                        session.add(articleCategory)

                    if body is not None:
                        if query is None or query[1] is None:
                            session.add(CrawlArticleBody(aid=article.id, body=body))
                        elif query[1] is not None:
                            session.query(CrawlArticleBody).filter(CrawlArticleBody.aid == article.id).update({"body":body})
            except Exception as e:
                self.logger.error('Catch an exception.', exc_info=True)