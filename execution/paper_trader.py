import logging

class PaperTrader:
    def __init__(self, starting_usdt, history_file="state/paper_trades.csv"):
        self.usdt = starting_usdt
        self.holdings = {}  # symbol -> {"qty": float, "avg_price": float}

    def buy(self, symbol, price, usd_amount):
        qty = round(usd_amount / price, 6)
        if usd_amount > self.usdt:
            logging.warning(f"PaperTrade: Not enough USDT to buy {symbol}")
            return None

        self.usdt -= usd_amount
        self.holdings[symbol] = {
            "qty": qty,
            "avg_price": price
        }
        logging.info(f"Paper BUY: {qty} {symbol} @ {price}")
        return {"qty": qty, "price": price}

    def sell(self, symbol, price):
        if symbol not in self.holdings:
            logging.warning(f"PaperTrade: No holdings for {symbol} to sell")
            return None

        qty = self.holdings[symbol]["qty"]
        proceeds = qty * price
        self.usdt += proceeds
        logging.info(f"Paper SELL: {qty} {symbol} @ {price} => ${proceeds:.2f}")
        del self.holdings[symbol]
        return {"qty": qty, "price": price, "proceeds": proceeds}

    def get_balance(self):
        return {
            "USDT": self.usdt,
            **{k: v["qty"] for k, v in self.holdings.items()}
        }
import logging
import time
import csv
import os

class PaperTrader:
    def __init__(self, starting_usdt, history_file="paper_trades.csv"):
        self.usdt = starting_usdt
        self.holdings = {}  # symbol -> {"qty": float, "avg_price": float}
        self.history_file = history_file
        self._init_csv()

    def _init_csv(self):
        if not os.path.exists(self.history_file):
            with open(self.history_file, mode='w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["timestamp", "side", "symbol", "qty", "price", "usdt_balance"])

    def _log_trade(self, side, symbol, qty, price):
        with open(self.history_file, mode='a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                time.strftime("%Y-%m-%d %H:%M:%S"),
                side,
                symbol,
                qty,
                price,
                round(self.usdt, 2)
            ])

    def buy(self, symbol, price, usd_amount):
        qty = round(usd_amount / price, 6)
        if usd_amount > self.usdt:
            logging.warning(f"PaperTrade: Not enough USDT to buy {symbol}")
            return None

        self.usdt -= usd_amount
        self.holdings[symbol] = {
            "qty": qty,
            "avg_price": price
        }
        self._log_trade("BUY", symbol, qty, price)
        logging.info(f"Paper BUY: {qty} {symbol} @ {price}")
        return {"qty": qty, "price": price}

    def sell(self, symbol, price):
        if symbol not in self.holdings:
            logging.warning(f"PaperTrade: No holdings for {symbol} to sell")
            return None

        qty = self.holdings[symbol]["qty"]
        proceeds = qty * price
        self.usdt += proceeds
        self._log_trade("SELL", symbol, qty, price)
        logging.info(f"Paper SELL: {qty} {symbol} @ {price} => ${proceeds:.2f}")
        del self.holdings[symbol]
        return {"qty": qty, "price": price, "proceeds": proceeds}

    def get_balance(self):
        return {
            "USDT": round(self.usdt, 2),
            **{k: round(v["qty"], 6) for k, v in self.holdings.items()}
        }
