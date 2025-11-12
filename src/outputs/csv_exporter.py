from __future__ import annotations
from typing import List, Dict, Any
from pathlib import Path
import csv

def export_csv(items: List[Dict[str, Any]], out_path: Path):
    out_path = Path(out_path)
    # Collect union of keys
    keys = set()
    for it in items:
        keys.update(it.keys())
    fieldnames = sorted(keys)
    with out_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for it in items:
            writer.writerow({k: it.get(k) for k in fieldnames})