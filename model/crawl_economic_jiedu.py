# -*- encoding: utf-8 -*-
"""
定义数据库模型实体 
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, func, Index, SmallInteger, DECIMAL, Date
from model.util import Base

class CrawlEconomicJiedu(Base):
    __tablename__ = 'jujin8_economic_jiedu'

    id = Column(Integer, primary_key=True, autoincrement=True)
    dataname_id = Column(Integer)
    next_pub_time = Column(String(128))
    pub_agent = Column(String(128))
    pub_frequency = Column(String(128))
    count_way = Column(String(256))
    data_influence = Column(String(512))
    data_define = Column(String(512))
    funny_read = Column(String(512))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    Index('idx_dataname_id', dataname_id)