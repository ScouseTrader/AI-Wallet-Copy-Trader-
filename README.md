# AI Wallet Copy Trader

## Setup

1. **Install Dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

2. **Configure Keys**:
    Copy `config.example.py` to `config.py`:

    ```bash
    cp config.example.py config.py
    ```

    Edit `config.py` (or use `.env`) with your API keys:
    * `BITQUERY_API_KEY` (Required for Analysis)

3. **Run**:

    ```bash
    python main.py
    ```

## Modules

* `scout.py`: Finds trending tokens using Birdeye.
* `brain.py`: Finds early buyers of those tokens using BitQuery & scores them.
* `copier.py`: (Mock) execution engine that would follow the top wallets.
