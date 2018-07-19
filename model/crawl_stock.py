# -*- encoding: utf-8 -*-
"""
定义数据库模型实体 
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, func, Index, SmallInteger
from model.util import Base

class CrawlStock(Base):
    """行情资讯类"""
    __tablename__ = 'jujin8_stock'

    id = Column(Integer, primary_key=True)
    publish_time = Column(String(22), nullable=True)
    position = Column(String(48), nullable=True)
    iod = Column(String(20), nullable=True)
    type = Column(SmallInteger, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    Index('index_pubish_time_type', type, publish_time)