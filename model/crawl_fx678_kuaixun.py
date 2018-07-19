# -*- encoding: utf-8 -*-
"""
定义数据库模型实体 
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, func, Index, SmallInteger, DECIMAL, Date
from model.util import Base

class CrawlFx678Kuaixun(Base):
    __tablename__ = 'jujin8_fx678_kuaixun'

    id = Column(Integer, primary_key=True)
    publish_time = Column(DateTime)
    body = Column(Text)
    time_detail = Column(String(32))
    importance = Column(SmallInteger)
    more_link = Column(String(255))
    image = Column(String(255))
    type = Column(SmallInteger)
    former_value = Column(String(32))
    predicted_value = Column(String(32))
    published_value = Column(String(32))
    country = Column(String(64))
    influnce = Column(String(64))
    star = Column(SmallInteger)
    source_id = Column(String(10))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
