# -*- encoding: utf-8 -*-
"""
定义数据库模型实体 
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, func, Index
from model.util import Base

class CrawlCategoryMap(Base):
    """行情资讯类"""
    __tablename__ = 'jujin8_category_map'

    id = Column(Integer, primary_key=True)
    source_category = Column(String(32))
    source_site = Column(String(32))
    target = Column(Integer)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())