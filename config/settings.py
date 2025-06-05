import os
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

# 🌍 ENVIRONMENT SELECTOR
# ✅ ENVIRONMENT: must be 'live' or 'testnet'
ENVIRONMENT = os.getenv("ENVIRONMENT")
if ENVIRONMENT is None:
    raise ValueError("Missing ENVIRONMENT in .env file — must be set to 'live' or 'testnet'.")

ENVIRONMENT = ENVIRONMENT.lower()
if ENVIRONMENT not in ("live", "testnet"):
    raise ValueError("Invalid ENVIRONMENT — must be 'live' or 'testnet'.")

if ENVIRONMENT == "live":
    API_KEY = os.getenv("BINANCE_API_KEY")
    API_SECRET = os.getenv("BINANCE_API_SECRET")
    BASE_URL = os.getenv("BINANCE_BASE_URL", "https://api.binance.com")
    TESTNET = False

elif ENVIRONMENT == "testnet":
    API_KEY = os.getenv("BINANCE_TESTNET_API_KEY")
    API_SECRET = os.getenv("BINANCE_TESTNET_API_SECRET")
    BASE_URL = os.getenv("BINANCE_TESTNET_BASE_URL", "https://testnet.binance.vision")
    TESTNET = True

else:
    raise ValueError("❌ Invalid ENVIRONMENT in .env — must be 'live' or 'testnet'")

# 📊 STRATEGY SETTINGS
STRATEGY_CONFIG = {
    "name": "mean_reversion",  # Options: "mean_reversion", "scalping"
    "mean_reversion": {
        "drop_threshold_pct": 1.0,
        "rebound_threshold_pct": 3.0,
        "lookback_period": 20
    },
    "scalping": {
        "grid_size": 0.2,
        "max_positions": 5
    }
}

# ⚙️ TRADING CONFIGURATION
TRADING_CONFIG = {
    "pair": os.getenv("TRADING_PAIR", "XRPUSDT"),
    "timeframe": os.getenv("TIMEFRAME", "1h"),
    "trade_amount_usd": float(os.getenv("TRADE_AMOUNT_USD", 20)),
    "testnet": TESTNET
}

# 🔑 BINANCE CONFIG
BINANCE_CONFIG = {
    "api_key": API_KEY,
    "api_secret": API_SECRET,
    "base_url": BASE_URL
}

# 📬 TELEGRAM CONFIG
TELEGRAM_CONFIG = {
    "bot_token": os.getenv("TELEGRAM_BOT_TOKEN"),
    "chat_id": os.getenv("TELEGRAM_CHAT_ID")
}
