from crypto_portfolio.api.debank_balances import DebankBalances
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()


wallet = os.getenv("STEELKEY_WALLET")
print(wallet)

api = DebankBalances()

balances_df = api.fetch_chain_balances(wallet_address=wallet, dataframe=True, quiet=True)
print(balances_df.head())

tokens_df = api.fetch_token_balances(wallet_address=wallet, dataframe=True)
print(tokens_df.head())

