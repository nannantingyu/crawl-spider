# -*- encoding: utf-8 -*-
"""
定义数据库模型实体 
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, func, Index
from model.util import Base

class CrawlCftc(Base):
    """行情资讯类"""
    __tablename__ = 'jujin8_cftc'

    id = Column(Integer, primary_key=True)
    cftc_name = Column(String(32))
    net_long = Column(Integer, nullable=True)
    net_short = Column(Integer, nullable=True)
    publish_time = Column(DateTime, nullable=True)
    publish_time_end = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    Index('index_publish_time_name', cftc_name, publish_time)