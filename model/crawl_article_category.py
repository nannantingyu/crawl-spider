# -*- encoding: utf-8 -*-
"""
定义数据库模型实体 
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, func, Index, SmallInteger
from model.util import Base

class CrawlArticleCategory(Base):
    """文章分类表"""
    __tablename__ = 'jujin8_article_category'

    aid = Column(Integer)
    cid = Column(Integer)