from config.settings import STRATEGY_CONFIG
import pandas as pd

class ScalpingStrategy:
    def __init__(self):
        self.config = STRATEGY_CONFIG["scalping"]
        self.grid_size_pct = self.config["grid_size"] / 100.0
        self.last_buy_price = None
        self.in_position = False

    def generate_signal(self, df: pd.DataFrame):
        if len(df) < 2:
            return "hold"

        current_price = df["close"].iloc[-1]
        prev_price = df["close"].iloc[-2]

        if not self.in_position:
            drop_pct = (prev_price - current_price) / prev_price
            if drop_pct >= self.grid_size_pct:
                self.last_buy_price = current_price
                self.in_position = True
                return "buy"
        else:
            gain_pct = (current_price - self.last_buy_price) / self.last_buy_price
            if gain_pct >= self.grid_size_pct:
                self.in_position = False
                self.last_buy_price = None
                return "sell"

        return "hold"
