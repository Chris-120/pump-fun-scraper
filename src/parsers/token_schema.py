from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

@dataclass
class PoolSnapshot:
    pool_name: str
    price: Optional[float] = None
    price_change_5m: Optional[float] = None
    price_change_15m: Optional[float] = None
    price_change_30m: Optional[float] = None
    price_change_1h: Optional[float] = None
    price_change_6h: Optional[float] = None
    price_change_24h: Optional[float] = None

@dataclass
class Token:
    mint: str
    name: Optional[str] = None
    symbol: Optional[str] = None
    description: Optional[str] = None
    creator: Optional[str] = None
    market_cap: Optional[float] = None
    usd_market_cap: Optional[float] = None
    created_timestamp: Optional[str] = None
    image_uri: Optional[str] = None
    metadata_uri: Optional[str] = None
    twitter: Optional[str] = None
    telegram: Optional[str] = None
    website: Optional[str] = None
    bonding_curve: Optional[str] = None
    associated_bonding_curve: Optional[str] = None
    raydium_pool: Optional[str] = None
    complete: bool = False
    virtual_sol_reserves: Optional[int] = None
    virtual_token_reserves: Optional[int] = None
    hidden: Optional[bool] = None
    total_supply: Optional[int] = None
    show_name: Optional[bool] = None
    last_trade_timestamp: Optional[str] = None
    king_of_the_hill_timestamp: Optional[str] = None
    reply_count: Optional[int] = None
    last_reply: Optional[str] = None
    nsfw: bool = False
    market_id: Optional[str] = None
    inverted: Optional[bool] = None
    is_currently_live: Optional[bool] = None
    username: Optional[str] = None
    profile_image: Optional[str] = None
    pool: Optional[PoolSnapshot] = None
    scraped_date: Optional[str] = None