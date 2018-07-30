# -*- encoding: utf-8 -*-
"""
定义数据库模型实体 
"""
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, func, Index, SmallInteger, TIMESTAMP
from model.util import Base

class CrawlBlockInfo(Base):
    """行情资讯类"""
    __tablename__ = 'jujin8_block_info'

    id = Column(Integer, primary_key=True)
    coin_id = Column(String(64))
    symbol = Column(String(64))
    cn_name = Column(String(64))
    en_name = Column(String(64))
    coin_name = Column(String(32))
    consensus = Column(String(32))
    available_supply = Column(String(30))
    total_supply = Column(String(30))
    max_supply = Column(String(30))
    available_price = Column(Float)
    volume_usd_24h = Column(Float)
    image = Column(String(256))
    trend_image = Column(Float)
    min_price_24h = Column(Float)
    max_price_24h = Column(Float)
    percent_change_1h = Column(Float)
    percent_change_1m = Column(Float)
    percent_change_1y = Column(Float)
    percent_change_24h = Column(Float)
    percent_change_3m = Column(Float)
    percent_change_7d = Column(Float)
    percent_change_all = Column(Float)
    percent_change_today = Column(Float)
    price_btc = Column(String(30))
    price_usd = Column(String(30))
    rank = Column(Integer)
    volume_rank = Column(Integer)
    founder = Column(String(30))
    forum = Column(Float)
    ico_date = Column(String(30))
    ico_price = Column(String(30))
    ico_price_usd = Column(String(30))
    icon = Column(String(255))
    repository = Column(String(255))
    mineable = Column(SmallInteger)
    algorithm = Column(String(30))
    explorer = Column(String(256))

    finance_buy_usd = Column(Float)
    finance_in_usd = Column(Float)
    finance_sell_usd = Column(Float)

    market_cap_usd = Column(Float)
    release_time = Column(String(10))

    total_market_cap_usd = Column(Float)
    websites = Column(String(512))

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
