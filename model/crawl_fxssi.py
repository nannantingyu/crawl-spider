# -*- encoding: utf-8 -*-
"""
定义数据库模型实体 
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, func, Index, Date
from model.util import Base

class CrawlFxssi(Base):
    """行情资讯类"""
    __tablename__ = 'jujin8_fxssi'

    id = Column(Integer, primary_key=True)
    broker = Column(String(32))
    pair = Column(String(32), nullable=True)
    val = Column(Float(2,2), nullable=True)
    day = Column(Date)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())