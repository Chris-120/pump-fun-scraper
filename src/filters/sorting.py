from __future__ import annotations
from typing import List
from dataclasses import asdict
from dateutil import parser as dtparser

def _safe_dt(value):
    try:
        return dtparser.parse(value) if value else None
    except Exception:
        return None

def _key_func(token, field: str):
    # Handle nested 'pool.price' style
    if field.startswith("pool."):
        _, sub = field.split(".", 1)
        pool = getattr(token, "pool", None)
        return getattr(pool, sub, None) if pool else None

    val = getattr(token, field, None)
    # Datetime fields
    if field.endswith("timestamp") or field in ("created_timestamp", "last_reply"):
        dt = _safe_dt(val)
        return dt.timestamp() if dt else float("-inf")
    # Fallback for dataclasses to avoid complex objects
    try:
        return val
    except Exception:
        return None

def sort_tokens(tokens: List, order_by: str = "created_timestamp", direction: str = "DESC") -> List:
    reverse = direction.upper() == "DESC"
    # Support known aliases
    if order_by in ("created_at", "created"):
        order_by = "created_timestamp"
    if order_by in ("last_trade", "last_trade_at"):
        order_by = "last_trade_timestamp"
    if order_by in ("last_reply_at",):
        order_by = "last_reply"

    tokens_sorted = sorted(tokens, key=lambda t: (_key_func(t, order_by) is None, _key_func(t, order_by)), reverse=reverse)
    return tokens_sorted