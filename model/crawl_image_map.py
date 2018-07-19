# -*- encoding: utf-8 -*-
"""
定义数据库模型实体 
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, func, Index
from model.util import Base

class CrawlImageMap(Base):
    """行情资讯类"""
    __tablename__ = 'jujin8_image_map'

    id = Column(Integer, primary_key=True)
    img_path = Column(String(300))
    real_path = Column(String(512))
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    Index('idx_image', img_path)