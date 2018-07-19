# -*- encoding: utf-8 -*-
"""
定义数据库模型实体 
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, func, Index, Date, SmallInteger, Text
from model.util import Base

class CrawlForexExchangeSpread(Base):
    """行情资讯类"""
    __tablename__ = 'jujin8_forex_exchange_spread'

    id = Column(Integer, primary_key=True)
    fid = Column(Integer)
    symble = Column(String(16))
    currency = Column(String(32))
    daily_spread = Column(Float)
    week_spread = Column(Float)
    month_spread = Column(Float)
    fee = Column(Float)

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())