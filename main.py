import time
import logging
import argparse

from execution.executor import TradeExecutor
from config.settings import TRADING_CONFIG

# Configure logging: to both console and file
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("state/bot.log", mode='a')
    ]
)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--live", action="store_true", help="Run in LIVE mode (overrides paper mode)")
    return parser.parse_args()

def show_mode_banner(paper_mode):
    if paper_mode:
        print("\n🧻 PAPER TRADING MODE ENABLED — NO REAL MONEY AT RISK 💸\n")
        logging.info("MODE: PAPER")
    else:
        print("\n🚨 LIVE TRADING MODE ENABLED — REAL FUNDS AT RISK ⚠️\n")
        logging.info("MODE: LIVE")

if __name__ == "__main__":
    args = parse_args()

    # Override paper trading mode if --live is passed
    if args.live:
        TRADING_CONFIG["paper_trading"] = False

    show_mode_banner(TRADING_CONFIG["paper_trading"])

    executor = TradeExecutor()

    # Show balances
    if TRADING_CONFIG["paper_trading"]:
        balance = executor.paper.get_balance()
        print(f"🧾 Starting Paper Balance: {balance}")
        logging.info(f"Paper Balance: {balance}")
        open_positions = executor.position_mgr.get_all_positions()
        if open_positions:
            print(f"📦 Resuming with open positions: {open_positions}")
            logging.info(f"Open positions loaded: {open_positions}")
    else:
        usdt = executor.api.get_asset_balance("USDT")
        print(f"💰 Live USDT Balance: {usdt}")
        logging.info(f"Live USDT Balance: {usdt}")

    # Start bot loop
    while True:
        executor.run_once()
        time.sleep(3600)  # Match with your candle timeframe (e.g., 900 for 15m)
