# python -m backtesting.optimize --symbol XRPUSDT --interval 1h --drop_start 1.0 --drop_end 3.0 --rebound_start 1.0 --rebound_end 3.0 --step 0.5


import pandas as pd
from brokers.binance_api import BinanceAPI
from strategies.mean_reversion import MeanReversionStrategy
import argparse

class Optimizer:
    def __init__(self, symbol, interval, limit=1000):
        self.symbol = symbol.upper()
        self.interval = interval
        self.limit = limit
        self.api = BinanceAPI()
        self.initial_balance = 1000.0

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

    def run_test(self, df, drop_pct, rebound_pct):
        usdt = self.initial_balance
        holdings = 0.0
        entry_price = None
        trade_log = []
        strategy = MeanReversionStrategy()
        strategy.drop_threshold = drop_pct / 100
        strategy.rebound_threshold = rebound_pct / 100

        for i in range(20, len(df)):  # using 20-period lookback
            window = df.iloc[:i + 1]
            signal = strategy.generate_signal(window)
            current_price = window["close"].iloc[-1]

            if signal == "buy" and usdt > 0:
                entry_price = current_price
                holdings = round(usdt / current_price, 6)
                usdt = 0
                trade_log.append(("BUY", current_price))

            elif signal == "sell" and holdings > 0:
                usdt = round(holdings * current_price, 2)
                trade_log.append(("SELL", current_price))
                holdings = 0
                entry_price = None

        final_balance = usdt + (holdings * (entry_price or 0))
        cumulative_return = ((final_balance - self.initial_balance) / self.initial_balance) * 100
        return {
            "drop": drop_pct,
            "rebound": rebound_pct,
            "trades": len(trade_log),
            "final_balance": round(final_balance, 2),
            "return_pct": round(cumulative_return, 2)
        }

    def optimize(self, drop_range, rebound_range):
        df = self.fetch_data()
        results = []

        print(f"\n🔍 Optimizing on {self.symbol} [{self.interval}], candles: {len(df)}\n")

        for drop in drop_range:
            for rebound in rebound_range:
                result = self.run_test(df.copy(), drop, rebound)
                results.append(result)
                print(f"Tested: drop={drop:.1f}%, rebound={rebound:.1f}% → return={result['return_pct']}%")

        results_df = pd.DataFrame(results)
        top = results_df.sort_values(by="return_pct", ascending=False).head(10)

        print(f"\n🏆 Top 10 Strategies for {self.symbol} ({self.interval}):")
        print(top.to_string(index=False))

# Helper for float range
def frange(start, stop, step):
    vals = []
    while start <= stop:
        vals.append(start)
        start = round(start + step, 10)
    return vals


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--symbol", type=str, default="XRPUSDT", help="Trading pair to optimize")
    parser.add_argument("--interval", type=str, default="1h", help="Candle timeframe (e.g. 15m, 1h)")
    parser.add_argument("--drop_start", type=float, default=1.0, help="Start drop %")
    parser.add_argument("--drop_end", type=float, default=3.0, help="End drop %")
    parser.add_argument("--rebound_start", type=float, default=1.0, help="Start rebound %")
    parser.add_argument("--rebound_end", type=float, default=3.0, help="End rebound %")
    parser.add_argument("--step", type=float, default=0.5, help="Step size for both params")

    args = parser.parse_args()

    drop_range = [round(x, 2) for x in frange(args.drop_start, args.drop_end, args.step)]
    rebound_range = [round(x, 2) for x in frange(args.rebound_start, args.rebound_end, args.step)]

    optimizer = Optimizer(symbol=args.symbol, interval=args.interval)
    optimizer.optimize(drop_range, rebound_range)


# Helper for float range
def frange(start, stop, step):
    vals = []
    while start <= stop:
        vals.append(start)
        start = round(start + step, 10)
    return vals
