from __future__ import annotations
from typing import Optional, Dict, Any
import requests
import math
import random

class RaydiumClient:
    """
    In offline mode, synthesizes a plausible pool snapshot with price and short-horizon changes.
    Online mode would query a price endpoint if configured.
    """

    def __init__(self, use_offline: bool = True, base_url: Optional[str] = None, timeout_s: int = 20):
        self.use_offline = use_offline
        self.base_url = base_url
        self.timeout_s = timeout_s

    def _offline_snapshot(self, pool_address: str, pool_name: str) -> Dict[str, Any]:
        # Deterministic random seeded by pool address to keep stable across runs
        seed = sum(ord(c) for c in pool_address) % 9973
        rng = random.Random(seed)

        price = max(1e-9, rng.random() * 1e-3)
        # Changes as percentages in [-99, +99]
        changes = {k: round(rng.uniform(-97.9, 97.9), 2) for k in ("5m", "15m", "30m", "1h", "6h", "24h")}
        return {
            "pool_name": pool_name,
            "price": price,
            "price_change_5m": changes["5m"],
            "price_change_15m": changes["15m"],
            "price_change_30m": changes["30m"],
            "price_change_1h": changes["1h"],
            "price_change_6h": changes["6h"],
            "price_change_24h": changes["24h"],
        }

    def get_pool_snapshot(self, pool_address: str, pool_name: str = "Token/SOL") -> Dict[str, Any]:
        if self.use_offline or not self.base_url:
            return self._offline_snapshot(pool_address, pool_name)

        # Example schema; real params depend on public API availability
        resp = requests.get(f"{self.base_url.rstrip('/')}/{pool_address}", timeout=self.timeout_s)
        resp.raise_for_status()
        data = resp.json()
        # Map/normalize the response
        return {
            "pool_name": data.get("pool_name", pool_name),
            "price": data.get("price"),
            "price_change_5m": data.get("price_change", {}).get("5m"),
            "price_change_15m": data.get("price_change", {}).get("15m"),
            "price_change_30m": data.get("price_change", {}).get("30m"),
            "price_change_1h": data.get("price_change", {}).get("1h"),
            "price_change_6h": data.get("price_change", {}).get("6h"),
            "price_change_24h": data.get("price_change", {}).get("24h"),
        }