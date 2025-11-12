import os
from pathlib import Path
from src.clients.pumpfun_client import PumpfunClient
from src.clients.raydium_client import RaydiumClient

def test_offline_clients():
    data_file = Path(__file__).resolve().parents[1] / "data" / "sample_output.json"
    pump = PumpfunClient(use_offline=True, offline_data_path=data_file)
    items = pump.list_tokens(limit=2, offset=0)
    assert isinstance(items, list) and len(items) == 2

    # Raydium offline snapshot should be deterministic for given address
    ray = RaydiumClient(use_offline=True)
    snap1 = ray.get_pool_snapshot("7Vux5xC9XZJ89gxRD2bUESjjtY4iRzihnEruVVG1Liag", "Bearly / SOL")
    snap2 = ray.get_pool_snapshot("7Vux5xC9XZJ89gxRD2bUESjjtY4iRzihnEruVVG1Liag", "Bearly / SOL")
    assert snap1["price"] == snap2["price"]
    assert snap1["pool_name"] == "Bearly / SOL"