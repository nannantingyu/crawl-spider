# -*- encoding: utf-8 -*-
"""
定义数据库模型实体 
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, func, Index, SmallInteger, DECIMAL, Date
from model.util import Base

class CrawlJinseKuaixun(Base):
    __tablename__ = 'jujin8_kuaixun_block'

    id = Column(Integer, primary_key=True)
    source_id = Column(Integer)
    title = Column(String(128))
    description = Column(String(255))
    keywords = Column(String(128))
    body = Column(String(1024))
    source_site = Column(String(32))
    publish_time = Column(DateTime)
    source_url = Column(String(256))
    type = Column(SmallInteger)
    status = Column(SmallInteger)
    importance = Column(SmallInteger)
    image = Column(String(512))
    link = Column(String(512))
    link_name = Column(String(32))

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())