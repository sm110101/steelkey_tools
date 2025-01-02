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
```

**Output Example

```plaintext
Interacted Chains:  ['op', 'arb', 'bsc', 'btt', 'eth', 'ftm', 'pls', 'base', 'celo', 'fuse', 'xdai', 'blast', 'matic']
```

```python
# Fetch chain balances as a DataFrame
chains_df = api.fetch_chain_balances(wallet, dataframe=True) # DataFrame=False returns the dictionary {chain_id: balance_usd, ...}
print(chains_df.head()) 
```

**Output Example**

```plaintext
  chain_id chain_name  chain_community_id         token_name                                    token_id  token_quantity  token_price    balance
0      arb   Arbitrum               42161           Balancer  0x040d1edc9569d4bab2d15287dc5a4f10f56a56b8        0.052954     2.635303   0.139550
1      arb   Arbitrum               42161        Black Agnus  0x306fd3e7b169aa4ee19412323e1a5995b8c1a1f4    30000.000000     0.000000   0.000000
2      arb   Arbitrum               42161            Radiant  0x3082cc23568ea640225c2467653db90e9250aaa0        2.295921     0.060921   0.139870
3      arb   Arbitrum               42161      Camelot token  0x3d9907f9a368ad0a51be60f7da3b97cf940982d8        0.001778   916.182213   1.629036
4      arb   Arbitrum               42161  Equilibria Pendle  0x3eabe18eae267d1b57f917aba085bb5906114600       33.710085     1.642202  55.358772
```

```python
# Fetch token balances by chain as a DataFrame
tokens_df = api.fetch_token_balances(wallet, dataframe=True)
print(tokens_df.head())
```
**Output Example**



