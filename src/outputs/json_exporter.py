from __future__ import annotations
from typing import List, Dict, Any
from pathlib import Path
import json

def export_json(items: List[Dict[str, Any]], out_path: Path):
    out_path = Path(out_path)
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)