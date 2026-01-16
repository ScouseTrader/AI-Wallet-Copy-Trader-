import time
import config


class Copier:
    def __init__(self):
        self.active_watchlist = []
        self.is_running = False

    def update_watchlist(self, wallets):
        """
        Updates the list of wallets to copy.
        """
        print(f"[Copier] Updating watchlist with {len(wallets)} wallets.")
        self.active_watchlist = wallets

    def start_listening(self):
        """
        Simulates listening for transactions from the active watchlist.
        For MVP, this is a loop that checks for 'signals' (mocked).
        In production, this would use a Web3 websocket subscription.
        """
        self.is_running = True
        print("[Copier] Started listening for trades...")

        try:
            while self.is_running:
                # 1. Listen for pending transactions
                # 2. If 'from' address in self.active_watchlist:
                #    3. Decode transaction
                #    4. If 'buy' method called:
                #       5. Execute Copy Trade

                # Mocking activity for demonstration
                # In real app, we would sleep less or use async
                time.sleep(2)

        except KeyboardInterrupt:
            self.stop_listening()

    def execute_copy_trade(self, signal):
        """
        Places a buy order for the token specified in the signal.
        """
        token = signal.get("token")
        amount = signal.get("amount_in_eth")
        from_wallet = signal.get("source_wallet")

        print(f"!!! COPY DETECTED !!!")
        print(f"Wallet {from_wallet} bought {token}")
        print(f"Executing BUY for {amount} ETH worth...")
        # Web3 buy logic would go here

    def stop_listening(self):
        self.is_running = False
        print("[Copier] Muted.")


if __name__ == "__main__":
    copier = Copier()
    copier.update_watchlist(["0x123...", "0xabc..."])
    # copier.start_listening() # Uncomment to test loop
