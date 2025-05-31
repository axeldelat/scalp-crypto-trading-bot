from data.market_data import MarketData

data = MarketData()
df = data.fetch_ohlcv(limit=50)

if df.empty:
    print("❌ No data returned. Check API connection or pair/timeframe config.")
else:
    print("✅ OHLCV Data (tail):")
    print(df.tail())
