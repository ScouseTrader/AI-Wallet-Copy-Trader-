import requests
import config
import datetime


class Brain:
    def __init__(self):
        self.url = "https://graphql.bitquery.io"
        self.headers = {
            "X-API-KEY": config.BITQUERY_API_KEY,
            "Content-Type": "application/json",
        }

    def find_early_buyers(self, token_address, limit=50):
        """
        Queries BitQuery for the first 'limit' buyers of a token.
        """
        query = """
        query ($token: String!, $limit: Int!) {
          ethereum(network: ethereum) {
            dexTrades(
              options: {limit: $limit, asc: "block.timestamp.time"}
              buyCurrency: {is: $token}
            ) {
              transaction {
                hash
              }
              taker {
                address
              }
              block {
                timestamp {
                  time
                }
              }
              buyAmount
            }
          }
        }
        """

        variables = {"token": token_address, "limit": limit}

        try:
            response = requests.post(
                self.url,
                json={"query": query, "variables": variables},
                headers=self.headers,
            )
            data = response.json()

            if "errors" in data:
                print(f"BitQuery Error: {data['errors']}")
                return []

            trades = data.get("data", {}).get("ethereum", {}).get("dexTrades", [])
            # Use 'taker' as the wallet address
            wallets = set([t["taker"]["address"] for t in trades if t.get("taker")])
            return list(wallets)

        except Exception as e:
            print(f"Exception in find_early_buyers: {e}")
            return []

    def score_wallets(self, wallets):
        """
        Analyzes a list of wallets and returns the ones with high 'Win Rate' and 'ROI'.
        For MVP, this is a mock implementation that simulates fetching history.
        """
        scored_wallets = []

        print(f"Analyzing {len(wallets)} wallets...")

        for wallet in wallets:
            # TODO: In a real implementation, we would query BitQuery again
            # to get the ENTIRE trade history of this wallet to calculate:
            # 1. Total Trades
            # 2. Profitable Trades
            # 3. Total PnL

            # Mocking score for testing
            # (We give a fake score between 0 and 100)
            mock_score = self._calculate_mock_score(wallet)

            if mock_score > 70:
                scored_wallets.append(
                    {
                        "address": wallet,
                        "score": mock_score,
                        "reason": "High Win Rate on recent pumps",
                    }
                )

        return sorted(scored_wallets, key=lambda x: x["score"], reverse=True)

    def _calculate_mock_score(self, wallet_address):
        # Deterministic mock score based on address string
        # This is just so we see diverse output in verification
        val = sum(ord(c) for c in wallet_address)
        return val % 100


if __name__ == "__main__":
    brain = Brain()
    if not config.BITQUERY_API_KEY:
        print("WARNING: BITQUERY_API_KEY not set.")

    # Test with a known token (e.g. PEPE on ETH)
    pepe_address = "0x6982508145454Ce325dDbE47a25d4ec3d2311933"

    print(f"Finding early buyers for PEPE ({pepe_address})...")
    buyers = brain.find_early_buyers(pepe_address, limit=10)

    if buyers:
        print(f"Found {len(buyers)} early buyers.")
        top_wallets = brain.score_wallets(buyers)
        print("Top Scored Wallets:")
        for w in top_wallets:
            print(f"Address: {w['address']} | Score: {w['score']}")
    else:
        print("No buyers found (check API key).")
