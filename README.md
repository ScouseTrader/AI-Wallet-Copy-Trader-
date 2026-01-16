# AI Wallet Copy Trader

## Setup

1. **Install Dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

2. **Configure Keys**:
    Edit `.env` (create it) or `config.py` with your API keys:
    * `BIRDEYE_API_KEY` (Free tier available)
    * `BITQUERY_API_KEY` (Free tier available)

3. **Run**:

    ```bash
    python main.py
    ```

## Modules

* `scout.py`: Finds trending tokens using Birdeye.
* `brain.py`: Finds early buyers of those tokens using BitQuery & scores them.
* `copier.py`: (Mock) execution engine that would follow the top wallets.
