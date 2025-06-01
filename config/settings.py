# Strategy and exchange settings
import os
from dotenv import load_dotenv

# Load API keys and secrets from .env
load_dotenv()

# Environment and account settings
API_KEY = os.getenv("BINANCE_API_KEY")  # TODO: Add real API key in .env
API_SECRET = os.getenv("BINANCE_API_SECRET")  # TODO: Add real secret in .env

# Strategy Settings
STRATEGY_CONFIG = {
    "name": "mean_reversion",  # Options: "mean_reversion", "scalping"
    "mean_reversion": {
        "drop_threshold_pct": 1.0,     # Buy when price drops > 5%
        "rebound_threshold_pct": 3.0, # Sell after 10% rebound
        "lookback_period": 20          # Periods to look back for average
    },
    "scalping": {
        "grid_size": 0.2,              # Price difference in percent for grid
        "max_positions": 5             # Max open scalping positions
    }
}

# Trade and Market Settings
TRADING_CONFIG = {
    "pair": "XRPUSDT",
    "timeframe": "1h",
    "trade_amount_usd": 20.0,
    "testnet": False,  # Set to True for testnet support
    "paper_trading": False,  # Toggle this to False for live trading
    "paper_balance_usdt": 250.0  # Starting simulated balance
}

# Binance API Config
BINANCE_CONFIG = {
    "api_key": API_KEY,
    "api_secret": API_SECRET,
    "base_url": "https://api.binance.com" if not TRADING_CONFIG["testnet"] else "https://testnet.binance.vision"
}
