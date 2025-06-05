# Executes trades based on signals
import logging
from data.market_data import MarketData
from strategies.mean_reversion import MeanReversionStrategy
from brokers.binance_api import BinanceAPI
from config.settings import TRADING_CONFIG
from execution.position_manager import PositionManager
from notifications.telegram import send_telegram_message

class TradeExecutor:
    def __init__(self):
        self.market_data = MarketData()
        self.strategy = MeanReversionStrategy()
        self.api = BinanceAPI()
        self.symbol = TRADING_CONFIG["pair"]
        self.trade_amount_usd = TRADING_CONFIG["trade_amount_usd"]
        self.position_mgr = PositionManager()

    def run_once(self):
        """Run one trading cycle: fetch data, get signal, execute trade."""
        df = self.market_data.fetch_ohlcv(limit=100)
        if df.empty:
            logging.warning("No market data available.")
            return

        signal = self.strategy.generate_signal(df)
        logging.info(f"Strategy signal: {signal}")

        if signal == "buy":
            self.execute_buy()
        elif signal == "sell":
            self.execute_sell()
        else:
            logging.info("Holding position...")

    def execute_buy(self):
        """Handle buy logic"""
        if self.position_mgr.has_position(self.symbol):
            logging.info("Buy skipped — already holding asset.")
            return

        price = self.api.get_symbol_price(self.symbol)
        if price is None:
            send_telegram_message(f"⚠️ Could not fetch price for {self.symbol}")
            return

        quantity = round(self.trade_amount_usd / price, 6)
        usdt_balance = self.api.get_asset_balance("USDT")

        if not usdt_balance or float(usdt_balance["free"]) < self.trade_amount_usd:
            msg = f"🚫 Insufficient USDT balance to BUY {self.symbol}."
            logging.warning(msg)
            send_telegram_message(msg)
            return

        result = self.api.place_market_order(self.symbol, "buy", quantity)
        if result:
            self.position_mgr.add_position(self.symbol, quantity, price)
            msg = f"🟢 *LIVE BUY* {self.symbol} | {quantity} @ {price:.4f}"
            logging.info(msg)
            send_telegram_message(msg)
        else:
            send_telegram_message(f"❌ *BUY failed* for {self.symbol}")

    def execute_sell(self):
        """Handle sell logic"""
        position = self.position_mgr.get_open_position(self.symbol)
        if not position:
            logging.info("No tracked position to sell.")
            return

        price = self.api.get_symbol_price(self.symbol)
        if price is None:
            send_telegram_message(f"⚠️ Could not fetch price for {self.symbol}")
            return

        quantity = round(position["qty"], 6)
        result = self.api.place_market_order(self.symbol, "sell", quantity)

        if result:
            self.position_mgr.close_position(self.symbol)
            msg = f"🔴 *LIVE SELL* {self.symbol} | {quantity} @ {price:.4f}"
            logging.info(msg)
            send_telegram_message(msg)
        else:
            send_telegram_message(f"❌ *SELL failed* for {self.symbol}")
