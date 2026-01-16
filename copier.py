import time
import json
import os
from datetime import datetime
from brain import Brain


class Copier:
    def __init__(self):
        self.active_watchlist = []
        self.is_running = False
        self.brain = Brain()
        self.signals_file = "signals.json"

        # Initialize signals file if not exists
        if not os.path.exists(self.signals_file):
            with open(self.signals_file, "w") as f:
                json.dump([], f)

    def update_watchlist(self, wallets):
        print(f"[Copier] Updating watchlist with {len(wallets)} wallets.")
        self.active_watchlist = wallets

    def start_listening(self):
        self.is_running = True
        print("[Copier] Started monitoring loop...")

        try:
            while self.is_running:
                print(f"[Copier] Scanning {len(self.active_watchlist)} wallets...")
                self._scan_and_log()

                # Sleep for 15 minutes (900 seconds)
                # For demo purposes, we can interrupt this loop or run it once in UI
                # But in a real daemon, it would wait.
                # In Streamlit, this loop blocks the UI.
                # Better approach for UI: Run one scan, then sleep or rely on manual refresh/cron.
                # For this implementation, we'll sleep briefly to allow stopping.
                for _ in range(900):
                    if not self.is_running:
                        break
                    time.sleep(1)

        except KeyboardInterrupt:
            self.stop_listening()

    def _scan_and_log(self):
        """
        Checks each wallet for recent trades and logs new ones.
        """
        new_signals = []

        for wallet in self.active_watchlist:
            recent_trades = self.brain.get_recent_trades(wallet, limit=1)

            for trade in recent_trades:
                # Simplified signal object
                timestamp = trade.get("block", {}).get("timestamp", {}).get("time")
                token_symbol = trade.get("buyCurrency", {}).get("symbol")
                amount = trade.get("buyAmount")
                tx_hash = trade.get("transaction", {}).get("hash")

                signal = {
                    "timestamp": timestamp,
                    "wallet": wallet,
                    "token": token_symbol,
                    "amount": amount,
                    "tx_hash": tx_hash,
                    "type": "BUY",
                }

                if self._is_new_signal(signal):
                    new_signals.append(signal)
                    print(f"New Signal: {wallet} bought {token_symbol}")

        if new_signals:
            self._save_signals(new_signals)

    def _is_new_signal(self, signal):
        # Check against existing signals to avoid duplicates
        try:
            with open(self.signals_file, "r") as f:
                existing = json.load(f)
                # Simple duplicate check by tx_hash
                existing_hashes = [s.get("tx_hash") for s in existing]
                return signal.get("tx_hash") not in existing_hashes
        except Exception:
            return True

    def _save_signals(self, new_signals):
        try:
            with open(self.signals_file, "r") as f:
                history = json.load(f)

            updated_history = new_signals + history

            with open(self.signals_file, "w") as f:
                json.dump(updated_history, f, indent=2)

        except Exception as e:
            print(f"Error saving signals: {e}")

    def stop_listening(self):
        self.is_running = False
        print("[Copier] Stopped.")
