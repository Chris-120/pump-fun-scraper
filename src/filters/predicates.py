from __future__ import annotations
from typing import Iterable, List
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
    name: str | None
    symbol: str | None
    description: str | None
    creator: str | None
    market_cap: float | None
    usd_market_cap: float | None
    created_timestamp: str | None
    image_uri: str | None
    metadata_uri: str | None
    twitter: str | None
    telegram: str | None
    website: str | None
    bonding_curve: str | None
    associated_bonding_curve: str | None
    raydium_pool: str | None
    complete: bool
    virtual_sol_reserves: int | None
    virtual_token_reserves: int | None
    hidden: bool | None
    total_supply: int | None
    show_name: bool | None
    last_trade_timestamp: str | None
    king_of_the_hill_timestamp: str | None
    reply_count: int | None
    last_reply: str | None
    nsfw: bool
    market_id: str | None
    inverted: bool | None
    is_currently_live: bool | None
    username: str | None
    profile_image: str | None
    pool: PoolSnapshot | None
    scraped_date: str | None

def filter_nsfw(tokens: Iterable[Token]) -> List[Token]:
    """Exclude tokens marked NSFW."""
    return [t for t in tokens if not getattr(t, "nsfw", False)]

def filter_min_market_cap(tokens: Iterable[Token], min_cap: float) -> List[Token]:
    """Keep tokens with market_cap (or usd_market_cap if present) >= min_cap."""
    out: List[Token] = []
    for t in tokens:
        cap = None
        # Prefer USD cap if available; else fall back to native cap
        if getattr(t, "usd_market_cap", None) is not None:
            cap = t.usd_market_cap
        elif getattr(t, "market_cap", None) is not None:
            cap = t.market_cap
        if cap is None:
            continue
        if cap >= min_cap:
            out.append(t)
    return out

def filter_graduated_only(tokens: Iterable[Token]) -> List[Token]:
    """Keep tokens where complete=True (graduated to Raydium)."""
    return [t for t in tokens if bool(getattr(t, "complete", False))]