from binance.client import Client
from dotenv import load_dotenv
import os

def test_signature():
    print("🔐 Running Signature Test...")

    load_dotenv()

    api_key = os.getenv("BINANCE_TESTNET_API_KEY")
    api_secret = os.getenv("BINANCE_TESTNET_API_SECRET")
    base_url = os.getenv("BINANCE_TESTNET_BASE_URL", "https://testnet.binance.vision")

    print("API Key:", api_key)
    print("Base URL:", base_url)

    if not api_key or not api_secret:
        print("❌ API key/secret not set in .env")
        return

    # ✅ Enable Testnet mode correctly using API_URL override + verify SSL option
    client = Client(api_key=api_key, api_secret=api_secret, tld='com', testnet=True)
    client.API_URL = base_url  # this must match the Testnet URL

    try:
        account = client.get_account()
        print("✅ Signature test successful: Account fetched")
        print(account)
    except Exception as e:
        print(f"❌ Signature test failed: {e}")

if __name__ == "__main__":
    test_signature()
