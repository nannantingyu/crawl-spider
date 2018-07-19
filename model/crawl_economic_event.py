# -*- encoding: utf-8 -*-
"""
定义数据库模型实体 
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, func, Index, SmallInteger, DECIMAL, Date
from model.util import Base

class CrawlEconomicEvent(Base):
    __tablename__ = 'jujin8_economic_event'

    id = Column(Integer, primary_key=True)
    country = Column(String(64))
    time = Column(String(512))
    city = Column(String(32))
    importance = Column(String(24))
    event = Column(String(256))
    date = Column(Date)
    source_id = Column(Integer)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())