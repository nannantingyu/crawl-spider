# -*- coding: utf-8 -*-
from model.crawl_article import CrawlArticle
from model.crawl_article_body import CrawlArticleBody
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

                    if body is not None:
                        if query is None or query[1] is None:
                            session.add(CrawlArticleBody(aid=article.id, body=body))
                        elif query[1] is not None:
                            session.query(CrawlArticleBody).filter(CrawlArticleBody.aid == article.id).update({"body":body})
            except Exception as e:
                self.logger.error('Catch an exception.', exc_info=True)