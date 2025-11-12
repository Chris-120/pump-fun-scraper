from src.parsers.transformers import to_token, token_to_flat_dict
from pathlib import Path
import json

def test_transform_and_flatten():
    path = Path(__file__).resolve().parents[1] / "data" / "sample_output.json"
    raw = json.loads(path.read_text(encoding="utf-8"))[0]
    token = to_token(raw)
    assert token.mint
    assert token.complete is True
    flat = token_to_flat_dict(token)
    assert "pool.price" in flat
    assert "mint" in flat and flat["mint"] == token.mint