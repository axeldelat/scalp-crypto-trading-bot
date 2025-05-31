# Executes trades based on signals
import time
from data.market_data import MarketData
from strategies.mean_reversion import MeanReversionStrategy
from brokers.binance_api import BinanceAPI
from config.settings import TRADING_CONFIG
import logging
from execution.position_manager import PositionManager
from execution.paper_trader import PaperTrader


class TradeExecutor:
    def __init__(self):
        self.market_data = MarketData()
        self.strategy = MeanReversionStrategy()
        self.api = BinanceAPI()
        self.symbol = TRADING_CONFIG["pair"]
        self.trade_amount_usd = TRADING_CONFIG["trade_amount_usd"]
        self.position_mgr = PositionManager()
        if TRADING_CONFIG["paper_trading"]:
            self.paper = PaperTrader(TRADING_CONFIG["paper_balance_usdt"])
        else:
            self.paper = None


    def run_once(self):
        """Run one trading cycle"""
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
        if self.position_mgr.has_position(self.symbol):
            logging.info("Buy skipped — already holding asset.")
            return

        price = self.api.get_symbol_price(self.symbol)
        if price is None:
            return

        if TRADING_CONFIG["paper_trading"]:
            trade = self.paper.buy(self.symbol, price, self.trade_amount_usd)
            if trade:
                self.position_mgr.add_position(self.symbol, trade["qty"], trade["price"])
        else:
            quantity = round(self.trade_amount_usd / price, 6)
            usdt_balance = self.api.get_asset_balance("USDT")
            if not usdt_balance or float(usdt_balance["free"]) < self.trade_amount_usd:
                logging.warning("Not enough USDT to buy.")
                return
            result = self.api.place_market_order(self.symbol, "buy", quantity)
            if result:
                self.position_mgr.add_position(self.symbol, quantity, price)
                logging.info(f"BUY order executed and position tracked: {quantity} @ {price}")



    def execute_sell(self):
        position = self.position_mgr.get_open_position(self.symbol)
        if not position:
            logging.info("No tracked position to sell.")
            return

        price = self.api.get_symbol_price(self.symbol)
        if price is None:
            return

        quantity = round(position["qty"], 6)

        if TRADING_CONFIG["paper_trading"]:
            self.paper.sell(self.symbol, price)
            self.position_mgr.close_position(self.symbol)
        else:
            result = self.api.place_market_order(self.symbol, "sell", quantity)
            if result:
                self.position_mgr.close_position(self.symbol)