# -*- encoding: utf-8 -*-
"""
定义数据库模型实体 
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, func, Index, SmallInteger
from model.util import Base

class CrawlCrawlArticle(Base):
    """行情资讯类"""
    __tablename__ = 'jujin8_crawl_article'

    id = Column(Integer, primary_key=True)
    url = Column(String(512))
    categories = Column(String(64))
    state = Column(SmallInteger)
    user_id = Column(Integer)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    Index('idx_source_url', url)