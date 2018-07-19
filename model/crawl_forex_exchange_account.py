# -*- encoding: utf-8 -*-
"""
定义数据库模型实体 
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, func, Index, Date, SmallInteger, Text
from model.util import Base

class CrawlForexExchangeAccount(Base):
    """行情资讯类"""
    __tablename__ = 'jujin8_forex_exchange_account'

    id = Column(Integer, primary_key=True)
    fid = Column(Integer)
    trade_species = Column(String(64))
    main_spread = Column(String(64))
    biggest_leverage = Column(String(16))
    explosion = Column(SmallInteger)
    lock_position = Column(SmallInteger)
    scalp = Column(SmallInteger)
    min_withdraw = Column(String(32))
    min_lots = Column(String(32))
    spread_type = Column(String(64))
    min_position = Column(String(32))
    ea = Column(SmallInteger)
    commission = Column(String(32))
    account_type = Column(String(255))

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())