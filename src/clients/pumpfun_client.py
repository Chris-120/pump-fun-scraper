from __future__ import annotations
from typing import List, Dict, Any, Optional
from pathlib import Path
import json
import requests

class PumpfunClient:
    """
    Minimal client. In offline mode, reads tokens from a local JSON file.
    In online mode, you may specify a public API endpoint via settings; if not provided, it raises.
    """

    def __init__(
        self,
        use_offline: bool = True,
        offline_data_path: Path | str | None = None,
        base_url: Optional[str] = None,
        timeout_s: int = 20,
    ):
        self.use_offline = use_offline
        self.offline_data_path = Path(offline_data_path) if offline_data_path else None
        self.base_url = base_url
        self.timeout_s = timeout_s

    def _read_offline(self) -> List[Dict[str, Any]]:
        if not self.offline_data_path or not self.offline_data_path.exists():
            raise FileNotFoundError(
                f"Offline data file not found at: {self.offline_data_path}"
            )
        with self.offline_data_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        # Accept either {"items": [...]} or a raw list
        if isinstance(data, dict) and "items" in data:
            return data["items"]
        if isinstance(data, list):
            return data
        raise ValueError("Unsupported offline JSON format")

    def list_tokens(
        self, limit: int = 100, offset: int = 0, order_by: str = "created_timestamp", direction: str = "DESC"
    ) -> List[Dict[str, Any]]:
        if self.use_offline:
            items = self._read_offline()
            # Basic deterministic slicing for pagination
            items = items[offset : offset + limit]
            return items

        if not self.base_url:
            raise RuntimeError(
                "Online mode requires a 'pumpfun_base_url' in settings or PUMPFUN_BASE_URL env."
            )

        # Example GET; the actual parameters depend on the real API
        params = {
            "limit": limit,
            "offset": offset,
            "order_by": order_by,
            "direction": direction,
        }
        resp = requests.get(self.base_url, params=params, timeout=self.timeout_s)
        resp.raise_for_status()
        payload = resp.json()
        if isinstance(payload, dict) and "items" in payload:
            return payload["items"]
        if isinstance(payload, list):
            return payload
        raise ValueError("Unexpected response structure from Pump.fun API")