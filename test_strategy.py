# test_strategy.py
from data.market_data import MarketData
from strategies.mean_reversion import MeanReversionStrategy

md = MarketData()
df = md.fetch_ohlcv(limit=100)

strategy = MeanReversionStrategy()
signal = strategy.generate_signal(df)
print(f"Signal: {signal}")
