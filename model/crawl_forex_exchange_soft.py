# -*- encoding: utf-8 -*-
"""
定义数据库模型实体 
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, func, Index, Date, SmallInteger, Text
from model.util import Base

class CrawlForexExchangeSoft(Base):
    """行情资讯类"""
    __tablename__ = 'jujin8_forex_exchange_soft'


    id = Column(Integer, primary_key=True)
    fid = Column(Integer)
    soft_type = Column(String(32))
    soft_addr = Column(String(256))

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())