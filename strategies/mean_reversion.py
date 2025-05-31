# Mean reversion strategy implementation
import pandas as pd
from config.settings import STRATEGY_CONFIG

class MeanReversionStrategy:
    def __init__(self):
        self.config = STRATEGY_CONFIG["mean_reversion"]
        self.drop_threshold = self.config["drop_threshold_pct"] / 100.0
        self.rebound_threshold = self.config["rebound_threshold_pct"] / 100.0
        self.lookback = self.config["lookback_period"]
        self.in_position = False
        self.entry_price = None

    def generate_signal(self, df: pd.DataFrame):
        """Return 'buy', 'sell', or 'hold' based on mean reversion logic"""

        if len(df) < self.lookback:
            return "hold"  # Not enough data

        # Compute rolling average and latest price
        recent_closes = df["close"].iloc[-self.lookback:]
        average_price = recent_closes.mean()
        current_price = df["close"].iloc[-1]

        if not self.in_position:
            drop_pct = (average_price - current_price) / average_price
            if drop_pct >= self.drop_threshold:
                self.in_position = True
                self.entry_price = current_price
                return "buy"
        else:
            gain_pct = (current_price - self.entry_price) / self.entry_price
            if gain_pct >= self.rebound_threshold:
                self.in_position = False
                self.entry_price = None
                return "sell"

        return "hold"
