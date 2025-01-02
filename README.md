# steelkey_tools


Welcome to **Steelkey Tools**, a Python project designed to streamline cryptocurrency portfolio management using the DeBank API. This package provides utilities for fetching, processing, and exporting data on token balances, asset values, debts, and staked tokens across multiple chains.

## Features

- Fetch interacted blockchain networks for a wallet.
- Retrieve token balances, including quantities and prices, organized by chain.
- Export token balances as a pandas DataFrame for further analysis.
- Lightweight and extensible for cryptocurrency portfolio analytics.

## Installation

### Prerequisites

- Python 3.6 or higher
- [pip](https://pip.pypa.io/en/stable/installation/)
- [DeBank API key](https://docs.cloud.debank.com/en/readme/open-api)

### Install Locally

1. Clone this repository

```bash
git clone https://github.com/sm110101/steelkey_tools.git
```

2. Navigate to project directory

```bash
cd path/to/directory
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

## Usage 

### Quick Start

1. Add your DeBank API key to a `.env` file in the project root

```env
DEBANK_KEY="your_api_key_here"
```

2. Import the `DebankAPI` class to fetch and analyze wallet data

***Example Usage***

```python
from crypto_portfolio.api.debank import DebankAPI

# Initialize API
api = DebankAPI()

# Define wallet address
wallet_address = "0xbb140caad2a312dcb2d1eaec02bb11b35816d39d"

# Get interacted chains
chains = api.fetch_interacted_chains(wallet, output=True) # output parameter is required for this function since it is mostly used to update cached data for other calls
print("Interacted chains: ", chains)

# Fetch chain balances as a DataFrame
chains_df = api.fetch_chain_balances(wallet, dataframe=True) # DataFrame=False returns the dictionary {chain_id: balance_usd, ...}
print(chains_df.head()) 

# Fetch token balances by chain as a DataFrame
tokens_df = api.fetch_token_balances(wallet, dataframe=True)
print(tokens_df.head())
```


