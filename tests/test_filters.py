import os
from pathlib import Path
from src.parsers.transformers import to_token
from src.filters.predicates import filter_nsfw, filter_min_market_cap, filter_graduated_only

def _load_sample():
    data_path = Path(__file__).resolve().parents[1] / "data" / "sample_output.json"
    import json
    with data_path.open("r", encoding="utf-8") as f:
        return json.load(f)

def test_filtering_pipeline():
    raw = _load_sample()
    tokens = [to_token(r) for r in raw]

    # Exclude NSFW
    safe = filter_nsfw(tokens)
    assert all(not t.nsfw for t in safe)
    assert len(safe) == 2  # one NSFW in sample

    # Min market cap
    filtered = filter_min_market_cap(safe, 1000)
    assert all((t.usd_market_cap or t.market_cap or 0) >= 1000 for t in filtered)
    assert any(t.mint == "hXiY1MPjbuuWCeg5AYUgAawqsmJkm7i9rw4W8vKpump" for t in filtered)

    # Graduated only
    grads = filter_graduated_only(filtered)
    assert all(t.complete for t in grads)