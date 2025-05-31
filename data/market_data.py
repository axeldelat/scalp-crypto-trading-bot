# Fetch historical and live data
import pandas as pd
from brokers.binance_api import BinanceAPI
from config.settings import TRADING_CONFIG

class MarketData:
    def __init__(self):
        self.api = BinanceAPI()
        self.symbol = TRADING_CONFIG["pair"]
        self.interval = TRADING_CONFIG["timeframe"]

    def fetch_ohlcv(self, limit=100):
        """Fetch OHLCV data and return as a DataFrame"""
        raw_klines = self.api.get_klines(self.symbol, self.interval, limit=limit)

        if not raw_klines:
            return pd.DataFrame()  # Return empty DataFrame on error

        df = pd.DataFrame(raw_klines, columns=[
            'timestamp', 'open', 'high', 'low', 'close', 'volume',
            'close_time', 'quote_asset_volume', 'num_trades',
            'taker_buy_base', 'taker_buy_quote', 'ignore'
        ])

        # Convert types
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)
        df = df[['open', 'high', 'low', 'close', 'volume']].astype(float)

        return df
