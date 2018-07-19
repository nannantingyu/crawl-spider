# -*- encoding: utf-8 -*-
"""
定义数据库模型实体 
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, func
from model.util import Base

class CrawlArticleBody(Base):
    __tablename__ = 'jujin8_article_body'

    aid = Column(Integer, primary_key=True)
    body = Column(Text)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())