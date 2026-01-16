import config
from scout import Scout
from brain import Brain
from copier import Copier


def main():
    print("=== AI Wallet Copy Trader v0.1 ===")

    # 1. Initialize Components
    scout = Scout()
    brain = Brain()
    copier = Copier()

    # Check keys
    if not config.BITQUERY_API_KEY:
        print("[!] Missing BITQUERY_API_KEY. Analysis will fail.")

    # 2. Run Discovery (Scout)
    print("\n--- Phase 1: Scout (Discovery) ---")
    trending_tokens = scout.get_trending_tokens(limit=5)

    if not trending_tokens:
        print("No trending tokens found or API error. Exiting.")
        return

    print(f"Found {len(trending_tokens)} trending tokens.")
    for t in trending_tokens:
        print(f"> {t['symbol']} ({t['address']})")

    # 3. Run Analysis (Brain)
    print("\n--- Phase 2: Brain (Analysis) ---")
    all_smart_wallets = []

    for token in trending_tokens:
        print(f"finding early buyers for {token['symbol']}...")
        buyers = brain.find_early_buyers(token["address"], limit=20)

        # Add to pool (deduplicate later)
        all_smart_wallets.extend(buyers)

    unique_wallets = list(set(all_smart_wallets))
    print(f"Identified {len(unique_wallets)} unique candidate wallets.")

    if unique_wallets:
        print("Scoring wallets...")
        ranked_wallets = brain.score_wallets(unique_wallets)

        top_picks = ranked_wallets[:5]
        print(f"\nTop {len(top_picks)} High-Performing Wallets:")
        for w in top_picks:
            print(f"Address: {w['address']} | Score: {w['score']}")

        # 4. Start Execution (Copier)
        print("\n--- Phase 3: Copier (Execution) ---")
        copier.update_watchlist([w["address"] for w in top_picks])

        response = input("Start listening for trades? (y/n): ")
        if response.lower() == "y":
            copier.start_listening()
        else:
            print("Done. Copy execution skipped.")

    else:
        print("No wallets found to analyze.")


if __name__ == "__main__":
    main()
