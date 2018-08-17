# -*- encoding: utf-8 -*-
"""
定义数据库模型实体 
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, func, Index, SmallInteger
from model.util import Base

class CrawlConfig(Base):
    """配置"""
    __tablename__ = 'jujin8_config'

    id = Column(Integer, primary_key=True)
    key = Column(String(32), nullable=True)
    value = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())