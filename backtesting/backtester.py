import pandas as pd
from brokers.binance_api import BinanceAPI
from strategies.mean_reversion import MeanReversionStrategy
from strategies.scalping import ScalpingStrategy
from config.settings import TRADING_CONFIG, STRATEGY_CONFIG


class Backtester:
    def __init__(self, symbol, interval, limit=500):
        self.api = BinanceAPI()
        self.symbol = symbol
        self.interval = interval
        self.limit = limit

        self.initial_balance = 1000.0
        self.usdt = self.initial_balance
        self.holdings = 0.0
        self.entry_price = None
        self.trade_log = []

        strategy_name = STRATEGY_CONFIG["name"]
        if strategy_name == "mean_reversion":
            self.strategy = MeanReversionStrategy()
        elif strategy_name == "scalping":
            self.strategy = ScalpingStrategy()
        else:
            raise ValueError(f"Unknown strategy: {strategy_name}")

    def fetch_data(self):
        klines = self.api.get_klines(self.symbol, self.interval, limit=self.limit)
        df = pd.DataFrame(klines, columns=[
            'timestamp', 'open', 'high', 'low', 'close', 'volume',
            'close_time', 'quote_asset_volume', 'num_trades',
            'taker_buy_base', 'taker_buy_quote', 'ignore'
        ])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)
        df = df[['open', 'high', 'low', 'close', 'volume']].astype(float)
        return df

    def run(self):
        df = self.fetch_data()
        self.start_date = df.index[0].strftime("%Y-%m-%d %H:%M")
        self.end_date = df.index[-1].strftime("%Y-%m-%d %H:%M")

        active_name = STRATEGY_CONFIG["name"]
        lookback = STRATEGY_CONFIG[active_name].get("lookback_period", 20)

        for i in range(lookback, len(df)):
            window = df.iloc[:i + 1]
            signal = self.strategy.generate_signal(window)

            current_price = window["close"].iloc[-1]

            if signal == "buy" and self.usdt > 0:
                self.entry_price = current_price
                self.holdings = round(self.usdt / current_price, 6)
                self.usdt = 0
                self.trade_log.append(("BUY", current_price))

            elif signal == "sell" and self.holdings > 0:
                self.usdt = round(self.holdings * current_price, 2)
                self.trade_log.append(("SELL", current_price))
                self.holdings = 0
                self.entry_price = None

        self.summary()

    def summary(self):
        final_balance = self.usdt + self.holdings * (self.entry_price or 0)
        cumulative_return = ((final_balance - self.initial_balance) / self.initial_balance) * 100

        print("\n📊 Backtest Summary:")
        print(f"Date Range:     {self.start_date} → {self.end_date}")
        print(f"Start Balance:  ${self.initial_balance:.2f}")
        print(f"End Balance:    ${final_balance:.2f}")
        print(f"Cumulative Return: {cumulative_return:.2f}%")
        print(f"Trades:         {len(self.trade_log)}")
        wins = self._count_winners()
        print(f"Winning Trades: {wins}/{len(self.trade_log)//2} ({(wins / max(len(self.trade_log)//2,1)) * 100:.1f}%)")

        print("\n📜 Trade Log:")
        for side, price in self.trade_log:
            print(f"{side} @ ${price:.6f}")



    def _count_winners(self):
        wins = 0
        for i in range(0, len(self.trade_log)-1, 2):
            buy_price = self.trade_log[i][1]
            sell_price = self.trade_log[i+1][1]
            if sell_price > buy_price:
                wins += 1
        return wins


if __name__ == "__main__":
    backtester = Backtester(
        symbol=TRADING_CONFIG["pair"],
        interval=TRADING_CONFIG["timeframe"],
        limit=900
    )
    backtester.run()
