# -*- encoding: utf-8 -*-
"""
定义数据库模型实体 
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, func, Index, Date, SmallInteger, Text
from model.util import Base

class CrawlForexExchangeInterest(Base):
    """行情资讯类"""
    __tablename__ = 'jujin8_forex_exchange_interest'

    id = Column(Integer, primary_key=True)
    fid = Column(Integer)
    symble = Column(String(16))
    currency = Column(String(64))
    buy_interest = Column(String(64))
    sell_interest = Column(String(16))
    buy_sell_diff = Column(SmallInteger)
    trade_time = Column(SmallInteger)

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())