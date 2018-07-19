# -*- encoding: utf-8 -*-
"""
定义数据库模型实体 
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, func, Index, SmallInteger
from model.util import Base

class CrawlCategory(Base):
    """文章分类表"""
    __tablename__ = 'jujin8_category'

    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    ename = Column(String(20))
    pid = Column(Integer)
    sequence = Column(Integer)
    target = Column(String(32))
    state = Column(SmallInteger)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())