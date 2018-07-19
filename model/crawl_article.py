# -*- encoding: utf-8 -*-
"""
定义数据库模型实体 
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, func
from model.util import Base

class CrawlArticle(Base):
    __tablename__ = 'jujin8_article'

    id = Column(Integer, primary_key=True)
    title = Column(String(128))
    publish_time = Column(DateTime)
    author = Column(String(32))
    hits = Column(Integer, default=0)
    favor = Column(Integer, default=0)
    recommend = Column(Integer, default=0)
    url = Column(String(256), default='')
    source_type = Column(String(32), default='crawl')
    description = Column(String(512))
    image = Column(String(512))
    type = Column(String(32))
    keywords = Column(String(128))
    source_id = Column(String(64))
    source_url = Column(String(512))
    source_site = Column(String(32))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())