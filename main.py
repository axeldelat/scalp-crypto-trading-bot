# main.py
import time
import logging
from execution.executor import TradeExecutor
from config.settings import ENVIRONMENT, TRADING_CONFIG

# --- Logging setup ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("state/bot.log", mode='a')
    ]
)

def show_banner():
    if ENVIRONMENT == "testnet":
        print("\n🧪 TESTNET MODE ACTIVE — SIMULATED TRADING\n")
        logging.info("MODE: TESTNET")
    elif ENVIRONMENT == "live":
        print("\n🚨 LIVE TRADING MODE ENABLED — REAL FUNDS AT RISK ⚠️\n")
        logging.info("MODE: LIVE")

def main():
    show_banner()
    executor = TradeExecutor()

    # Show balance info only in LIVE mode
    if ENVIRONMENT != "testnet":
        usdt = executor.api.get_asset_balance("USDT")
        if usdt:
            print(f"💰 USDT Balance: {usdt}")
            logging.info(f"USDT Balance: {usdt}")
    else:
        logging.info("⏭️ Skipping balance fetch in testnet mode.")

    open_positions = executor.position_mgr.get_all_positions()
    if open_positions:
        print(f"📦 Resuming with open positions: {open_positions}")
        logging.info(f"Open positions loaded: {open_positions}")

    # --- Start bot loop ---
    while True:
        executor.run_once()
        time.sleep(3600)  # 1-hour interval

if __name__ == "__main__":
    main()
