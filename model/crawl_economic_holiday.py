# -*- encoding: utf-8 -*-
"""
定义数据库模型实体 
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, func, Index, SmallInteger, DECIMAL, Date
from model.util import Base

class CrawlEconomicHoliday(Base):
    __tablename__ = 'jujin8_economic_holiday'

    id = Column(Integer, primary_key=True)
    country = Column(String(64))
    time = Column(String(64))
    market = Column(String(32))
    holiday_name = Column(String(24))
    detail = Column(String(512))
    date = Column(Date)
    source_id = Column(Integer)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())