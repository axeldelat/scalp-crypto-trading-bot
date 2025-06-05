# brokers/binance_api.py
from binance.client import Client
from config.settings import BINANCE_CONFIG, TRADING_CONFIG
import logging
import requests

class BinanceAPI:
    def __init__(self):
        api_key = BINANCE_CONFIG["api_key"]
        api_secret = BINANCE_CONFIG["api_secret"]
        base_url = BINANCE_CONFIG["base_url"]
        self.use_testnet = TRADING_CONFIG["testnet"]

        self.client = Client(api_key=api_key, api_secret=api_secret)

        if self.use_testnet:
            self.client.API_URL = base_url
            self.client._base_endpoint = base_url
            self.client._api_url = base_url

        env = "TESTNET" if self.use_testnet else "LIVE"
        logging.info(f"🌐 Using Binance {env} API: {base_url}")

    def get_asset_balance(self, asset: str) -> float:
        try:
            balance_info = self.client.get_asset_balance(asset=asset)
            if balance_info:
                return float(balance_info['free'])
        except Exception as e:
            logging.warning(f"Direct asset balance failed for {asset}, trying fallback: {e}")

        try:
            account_info = self.client.get_account()
            for b in account_info['balances']:
                if b['asset'] == asset:
                    return float(b['free'])
        except Exception as e:
            logging.error(f"Failed to fetch fallback balance for asset {asset}: {e}")

        return 0.0

    def get_klines(self, symbol: str, interval: str, limit: int = 100):
        """
        Fetch OHLCV candlestick data using direct REST API call (compatible with testnet).
        """
        try:
            base_url = "https://testnet.binance.vision" if self.use_testnet else "https://api.binance.com"
            url = f"{base_url}/api/v3/klines"
            params = {
                "symbol": symbol,
                "interval": interval,
                "limit": limit
            }
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logging.error(f"Error fetching klines for {symbol} at {interval}: {e}")
            return []
