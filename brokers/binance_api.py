# Binance API interface (data + orders)
from binance.client import Client
from binance.enums import *
from config.settings import BINANCE_CONFIG, TRADING_CONFIG
import logging

class BinanceAPI:
    def __init__(self):
        self.client = Client(
            api_key=BINANCE_CONFIG["api_key"],
            api_secret=BINANCE_CONFIG["api_secret"]
        )

        # Optional: set testnet endpoint if using testnet
        if TRADING_CONFIG["testnet"]:
            self.client.API_URL = BINANCE_CONFIG["base_url"]

    def get_klines(self, symbol: str, interval: str, limit: int = 100):
        """Fetch OHLCV candles"""
        try:
            return self.client.get_klines(
                symbol=symbol,
                interval=interval,
                limit=limit
            )
        except Exception as e:
            logging.error(f"Error fetching klines: {e}")
            return []

    def get_asset_balance(self, asset: str):
        """Get balance of a specific asset"""
        try:
            return self.client.get_asset_balance(asset=asset)
        except Exception as e:
            logging.error(f"Error fetching balance: {e}")
            return None

    def place_market_order(self, symbol: str, side: str, quantity: float):
        """Execute a market order"""
        try:
            return self.client.create_order(
                symbol=symbol,
                side=SIDE_BUY if side.lower() == "buy" else SIDE_SELL,
                type=ORDER_TYPE_MARKET,
                quantity=quantity
            )
        except Exception as e:
            logging.error(f"Order failed: {e}")
            return None

    def get_symbol_price(self, symbol: str):
        """Get latest price for symbol"""
        try:
            return float(self.client.get_symbol_ticker(symbol=symbol)["price"])
        except Exception as e:
            logging.error(f"Error fetching price: {e}")
            return None
