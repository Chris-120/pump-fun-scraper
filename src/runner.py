import argparse
import json
import os
import sys
from pathlib import Path
from datetime import datetime, timezone

# Ensure sibling namespaces import correctly (PEP 420 implicit namespace packages)
SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from filters.predicates import (
    filter_nsfw,
    filter_min_market_cap,
    filter_graduated_only,
)
from filters.sorting import sort_tokens
from clients.pumpfun_client import PumpfunClient
from clients.raydium_client import RaydiumClient
from parsers.transformers import to_token, token_to_flat_dict
from outputs.json_exporter import export_json
from outputs.csv_exporter import export_csv

def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

def run_cli():
    parser = argparse.ArgumentParser(
        description="Pump.fun Token Scraper - offline/online runner"
    )
    parser.add_argument(
        "--config",
        default=str(SCRIPT_DIR / "config" / "settings.example.json"),
        help="Path to settings JSON",
    )
    parser.add_argument(
        "--input",
        default=str(SCRIPT_DIR.parent.parent / "data" / "inputs.sample.json"),
        help="Path to input JSON describing filters/sort/pagination",
    )
    parser.add_argument(
        "--export",
        choices=["json", "csv"],
        default=None,
        help="Override export format (json|csv). If omitted, uses input file setting.",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Override output file path. If omitted, uses input file setting.",
    )
    args = parser.parse_args()

    settings = load_json(Path(args.config))
    inputs = load_json(Path(args.input))

    # Environment overrides for convenience
    use_offline = bool(
        str(os.getenv("USE_OFFLINE", settings.get("use_offline", "true"))).lower()
        in ("1", "true", "yes")
    )
    data_file = Path(
        os.getenv("OFFLINE_DATA_PATH", settings.get("offline_data_path", ""))
    )
    if not data_file:
        # Default to repo data/sample_output.json if not set
        data_file = SCRIPT_DIR.parent.parent / "data" / "sample_output.json"

    export_kind = args.export or inputs.get("export", "json")
    out_path = Path(args.output or inputs.get("output", "output.json")).resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Instantiate clients
    pump_client = PumpfunClient(
        use_offline=use_offline,
        offline_data_path=data_file,
        base_url=settings.get("pumpfun_base_url"),
        timeout_s=settings.get("http_timeout_s", 20),
    )
    raydium_client = RaydiumClient(
        use_offline=use_offline,
        base_url=settings.get("raydium_base_url"),
        timeout_s=settings.get("http_timeout_s", 20),
    )

    # Pull raw tokens
    limit = int(inputs.get("limit", 100))
    offset = int(inputs.get("offset", 0))
    order_by = inputs.get("order_by", "created_timestamp")
    direction = inputs.get("order_by_direction", "DESC").upper()
    include_nsfw = bool(inputs.get("includeNsfw", False))
    min_cap = inputs.get("minMarketCap")
    graduated_only = bool(inputs.get("graduatedOnly", False))

    raw_tokens = pump_client.list_tokens(
        limit=limit,
        offset=offset,
        order_by=order_by,
        direction=direction,
    )

    # Transform and enrich
    tokens = [to_token(t) for t in raw_tokens]

    # Filtering pipeline
    if not include_nsfw:
        tokens = filter_nsfw(tokens)
    if min_cap is not None:
        tokens = filter_min_market_cap(tokens, float(min_cap))
    if graduated_only:
        tokens = filter_graduated_only(tokens)

    # Optional Raydium enrichment (only for graduated tokens)
    enriched = []
    for t in tokens:
        if t.complete and t.raydium_pool:
            t.pool = raydium_client.get_pool_snapshot(t.raydium_pool, t.symbol or t.name or "UNKNOWN")
        # Stamp scrape time if not set
        t.scraped_date = datetime.now(timezone.utc).isoformat()
        enriched.append(t)

    # Sorting (after enrichment so derived fields can be considered)
    enriched = sort_tokens(enriched, order_by=order_by, direction=direction)

    # Flatten for exporters
    flat = [token_to_flat_dict(t) for t in enriched]

    # Export
    if export_kind == "json":
        export_json(flat, out_path)
    elif export_kind == "csv":
        export_csv(flat, out_path)
    else:
        raise ValueError(f"Unknown export format: {export_kind}")

    print(f"Saved {len(flat)} tokens to {out_path}")

if __name__ == "__main__":
    run_cli()