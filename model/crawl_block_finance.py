# -*- encoding: utf-8 -*-
"""
定义数据库模型实体 
"""
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, func, Index, SmallInteger, TIMESTAMP
from model.util import Base

class CrawlBlockFinance(Base):
    """行情资讯类"""
    __tablename__ = 'jujin8_block_finance'

    id = Column(Integer, primary_key=True)
    coin_id = Column(String(64))
    price = Column(Float)

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
