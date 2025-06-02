# test_quantity.py

import math
from brokers.binance_api import BinanceAPI
from config.settings import TRADING_CONFIG

symbol = TRADING_CONFIG["pair"]
usd_amount = TRADING_CONFIG["trade_amount_usd"]

api = BinanceAPI()

def get_step_size(symbol):
    """Get step size for a symbol from Binance filters"""
    info = api.client.get_symbol_info(symbol)
    for f in info["filters"]:
        if f["filterType"] == "LOT_SIZE":
            return float(f["stepSize"])
    return 1.0  # fallback

def adjust_qty(qty, step):
    precision = int(round(-math.log10(step)))
    return round(math.floor(qty / step) * step, precision)

price = api.get_symbol_price(symbol)
if price is None:
    print(f"❌ Failed to fetch price for {symbol}")
else:
    qty = usd_amount / price
    step_size = get_step_size(symbol)
    adjusted_qty = adjust_qty(qty, step_size)

    print(f"📈 Price of {symbol}: {price}")
    print(f"💵 USD Amount: {usd_amount}")
    print(f"📦 Raw Quantity: {qty}")
    print(f"✅ Adjusted Quantity (LOT_SIZE): {adjusted_qty}")
