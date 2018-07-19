# -*- encoding: utf-8 -*-
"""
定义数据库模型实体 
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, func, Index, Date, SmallInteger, Text
from model.util import Base

class CrawlForexExchangeWithdraw(Base):
    """行情资讯类"""
    __tablename__ = 'jujin8_forex_exchange_withdraw'

    id = Column(Integer, primary_key=True)
    fid = Column(Integer)
    withdraw_way = Column(String(32))
    deposit_way = Column(String(32))
    withdraw_time = Column(String(32))
    deposit_time = Column(String(32))
    withdraw_fee = Column(String(32))
    deposit_fee = Column(String(32))
    withdraw_rate = Column(String(32))
    deposit_rate = Column(String(32))

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())