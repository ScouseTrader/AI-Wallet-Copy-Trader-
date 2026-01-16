import requests
import config


class Scout:
    def __init__(self):
        # GeckoTerminal API (Free, rate limited)
        self.base_url = "https://api.geckoterminal.com/api/v2"
        self.headers = {"Accept": "application/json;version=20230302"}
        # Mapping config.TARGET_CHAIN to GeckoTerminal network slugs
        self.chain_map = {"ethereum": "eth", "solana": "solana", "base": "base"}

    def get_trending_tokens(self, limit=10):
        """
        Fetches trending pools from GeckoTerminal.
        Returns a list of token dictionaries.
        """
        chain_slug = self.chain_map.get(config.TARGET_CHAIN, "eth")
        endpoint = f"/networks/{chain_slug}/trending_pools"

        try:
            url = f"{self.base_url}{endpoint}"
            # GeckoTerminal provides paginated included data, but trending pools
            # usually returns the pools directly in 'data'.

            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            data = response.json()

            pools = data.get("data", [])
            return self._process_pools(pools, limit)

        except Exception as e:
            print(f"Exception in get_trending_tokens: {e}")
            return []

    def _process_pools(self, pools, limit):
        """
        Extracts token info from pool data.
        GeckoTerminal returns pools, so we extract the base token.
        """
        qualified_tokens = []

        for pool in pools:
            if len(qualified_tokens) >= limit:
                break

            attributes = pool.get("attributes", {})

            # Filter by volume/liquidity if provided in attributes
            # GeckoTerminal response structure:
            # attributes: { volume_usd: { h24: "..." }, reserve_in_usd: "..." }

            try:
                vol_24h = float(attributes.get("volume_usd", {}).get("h24", 0))
                liquidity = float(attributes.get("reserve_in_usd", 0))
            except (ValueError, TypeError):
                continue

            if (
                liquidity >= config.MIN_LIQUIDITY_USD
                and vol_24h >= config.MIN_VOLUME_24H
            ):
                # Get Base Token ID (Address)
                # attributes.address is the POOL address
                # relationships.base_token.data.id might be "eth_0x..."

                # A simpler way is to grab the name/symbol from the pool name usually
                # But let's look at the structure carefully.
                # Usually: name = "TOKEN / ETH"

                token_name = attributes.get("name", "").split("/")[0].strip()

                # For address, we rely on the attributes or relationships
                # The 'base_token_price_usd' is there, but address needs parsing or additional call.
                # However, for MVP, let's use the POOL address or try to find token address.
                # Actually, attributes['address'] is the POOL address.
                # We need the TOKEN address for BitQuery.
                # GeckoTerminal v2 response usually includes 'relationships' -> 'base_token'.
                # But we might need to fetch the token details.

                # Workaround: For now, we return the POOL address as a proxy,
                # OR we try to extract if available.
                # Better: Use the 'base_token_id' if available in recent API versions.
                # Checking sample response structure: unfortunately typically requires second call or parsing ID.
                # relationships: { base_token: { data: { id: "eth_0x123..." } } }

                base_token_id_str = (
                    pool.get("relationships", {})
                    .get("base_token", {})
                    .get("data", {})
                    .get("id", "")
                )
                if "_" in base_token_id_str:
                    token_address = base_token_id_str.split("_")[1]
                else:
                    token_address = base_token_id_str

                if token_address:
                    qualified_tokens.append(
                        {
                            "symbol": token_name,
                            "address": token_address,
                            "price": attributes.get("base_token_price_usd"),
                            "liquidity": liquidity,
                            "volume24h": vol_24h,
                            "pool_address": attributes.get("address"),
                        }
                    )

        return qualified_tokens


if __name__ == "__main__":
    scout = Scout()
    print("Fetching trending tokens from GeckoTerminal...")
    trending = scout.get_trending_tokens()
    for t in trending:
        print(f"Found: {t['symbol']} ({t['address']}) | Liq: ${t['liquidity']:,.0f}")
