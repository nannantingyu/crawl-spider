# -*- encoding: utf-8 -*-
"""
定义数据库模型实体 
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, func, Index, SmallInteger, DECIMAL, Date
from model.util import Base

class CrawlWallstreetcnKuaixun(Base):
    __tablename__ = 'jujin8_wallstreetcn_kuaixun'

    id = Column(Integer, primary_key=True)
    publish_time = Column(DateTime)
    body = Column(Text)
    time_detail = Column(String(32))
    dateid = Column(String(20))
    importance = Column(SmallInteger)
    more_link = Column(String(255))
    image = Column(String(255))
    t0 = Column(String(32))
    t5 = Column(String(32))
    t7 = Column(String(128))
    t8 = Column(String(128))
    t10 = Column(String(128))
    t12 = Column(String(128))
    type = Column(SmallInteger)
    real_time = Column(String(12))
    typename = Column(String(32))
    former_value = Column(String(32))
    predicted_value = Column(String(32))
    published_value = Column(String(32))
    country = Column(String(64))
    influnce = Column(String(64))
    star = Column(SmallInteger)
    calendar_id = Column(String(10))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
