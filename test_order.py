from brokers.binance_api import BinanceAPI

# Initialize API wrapper
api = BinanceAPI()

# Settings
symbol = "XRPUSDT"
usd_amount = 20  # Amount in USDT to spend

# Create market buy order using quoteOrderQty
try:
    order = api.client.create_order(
        symbol=symbol,
        side="BUY",
        type="MARKET",
        quoteOrderQty=usd_amount  # ✅ Spend $20 worth of USDT
    )
    print("✅ Order successful:")
    print(order)
except Exception as e:
    print("❌ Order failed:")
    print(e)