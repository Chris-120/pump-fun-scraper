from __future__ import annotations
from typing import Dict, Any
from .token_schema import Token, PoolSnapshot

def to_token(raw: Dict[str, Any]) -> Token:
    """Map a raw dict (from Pump.fun) into a Token dataclass."""
    pool = None
    if isinstance(raw.get("pool"), dict):
        p = raw["pool"]
        pool = PoolSnapshot(
            pool_name=p.get("pool_name") or f"{raw.get('symbol') or raw.get('name') or 'Token'} / SOL",
            price=p.get("price"),
            price_change_5m=p.get("price_change_5m"),
            price_change_15m=p.get("price_change_15m"),
            price_change_30m=p.get("price_change_30m"),
            price_change_1h=p.get("price_change_1h"),
            price_change_6h=p.get("price_change_6h"),
            price_change_24h=p.get("price_change_24h"),
        )

    return Token(
        mint=raw.get("mint", ""),
        name=raw.get("name"),
        symbol=raw.get("symbol"),
        description=raw.get("description"),
        creator=raw.get("creator"),
        market_cap=raw.get("market_cap"),
        usd_market_cap=raw.get("usd_market_cap"),
        created_timestamp=raw.get("created_timestamp"),
        image_uri=raw.get("image_uri"),
        metadata_uri=raw.get("metadata_uri"),
        twitter=raw.get("twitter"),
        telegram=raw.get("telegram"),
        website=raw.get("website"),
        bonding_curve=raw.get("bonding_curve"),
        associated_bonding_curve=raw.get("associated_bonding_curve"),
        raydium_pool=raw.get("raydium_pool"),
        complete=bool(raw.get("complete", False)),
        virtual_sol_reserves=raw.get("virtual_sol_reserves"),
        virtual_token_reserves=raw.get("virtual_token_reserves"),
        hidden=raw.get("hidden"),
        total_supply=raw.get("total_supply"),
        show_name=raw.get("show_name"),
        last_trade_timestamp=raw.get("last_trade_timestamp"),
        king_of_the_hill_timestamp=raw.get("king_of_the_hill_timestamp"),
        reply_count=raw.get("reply_count"),
        last_reply=raw.get("last_reply"),
        nsfw=bool(raw.get("nsfw", False)),
        market_id=raw.get("market_id"),
        inverted=raw.get("inverted"),
        is_currently_live=raw.get("is_currently_live"),
        username=raw.get("username"),
        profile_image=raw.get("profile_image"),
        pool=pool,
        scraped_date=raw.get("scraped_date"),
    )

def token_to_flat_dict(t: Token) -> Dict[str, Any]:
    """Flatten Token + PoolSnapshot for JSON/CSV export."""
    pool = t.pool or PoolSnapshot(pool_name=None)
    return {
        "mint": t.mint,
        "name": t.name,
        "symbol": t.symbol,
        "description": t.description,
        "creator": t.creator,
        "market_cap": t.market_cap,
        "usd_market_cap": t.usd_market_cap,
        "created_timestamp": t.created_timestamp,
        "image_uri": t.image_uri,
        "metadata_uri": t.metadata_uri,
        "twitter": t.twitter,
        "telegram": t.telegram,
        "website": t.website,
        "bonding_curve": t.bonding_curve,
        "associated_bonding_curve": t.associated_bonding_curve,
        "raydium_pool": t.raydium_pool,
        "complete": t.complete,
        "virtual_sol_reserves": t.virtual_sol_reserves,
        "virtual_token_reserves": t.virtual_token_reserves,
        "hidden": t.hidden,
        "total_supply": t.total_supply,
        "show_name": t.show_name,
        "last_trade_timestamp": t.last_trade_timestamp,
        "king_of_the_hill_timestamp": t.king_of_the_hill_timestamp,
        "reply_count": t.reply_count,
        "last_reply": t.last_reply,
        "nsfw": t.nsfw,
        "market_id": t.market_id,
        "inverted": t.inverted,
        "is_currently_live": t.is_currently_live,
        "username": t.username,
        "profile_image": t.profile_image,
        "pool.pool_name": pool.pool_name,
        "pool.price": pool.price,
        "pool.price_change_5m": pool.price_change_5m,
        "pool.price_change_15m": pool.price_change_15m,
        "pool.price_change_30m": pool.price_change_30m,
        "pool.price_change_1h": pool.price_change_1h,
        "pool.price_change_6h": pool.price_change_6h,
        "pool.price_change_24h": pool.price_change_24h,
        "scraped_date": t.scraped_date,
    }