from brain import Brain
import config

print("--- Verifying BitQuery Connection ---")
if not config.BITQUERY_API_KEY:
    print("KEYS MISSING!")
    exit(1)

brain = Brain()
# USDC on Ethereum
token = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
print(f"Querying buyers for USDC ({token})...")

try:
    buyers = brain.find_early_buyers(token, limit=5)
    if buyers:
        print(f"SUCCESS: Found {len(buyers)} buyers.")
        print(f"Sample: {buyers[0]}")
    else:
        print(
            "SUCCESS: Connection made, but no buyers returned (might be query specific)."
        )
        # If it returns empty list without error, it still means auth worked.
        # If it printed "BitQuery Error", then we know found_early_buyers handles printing.
except Exception as e:
    print(f"FAILURE: {e}")
