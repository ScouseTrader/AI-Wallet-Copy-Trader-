import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
# BIRDEYE_API_KEY = "Not Required (Using GeckoTerminal Free API)"
BITQUERY_API_KEY = os.getenv("BITQUERY_API_KEY", "YOUR_BITQUERY_KEY_HERE")
MORALIS_API_KEY = os.getenv("MORALIS_API_KEY", "")

# Configuration
TARGET_CHAIN = "ethereum"  # or "solana", "base"
MIN_LIQUIDITY_USD = 10000
MIN_VOLUME_24H = 50000

# Scoring Weights
WEIGHT_WIN_RATE = 0.4
WEIGHT_ROI = 0.4
WEIGHT_AGE = 0.2
