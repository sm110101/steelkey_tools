from crypto_portfolio.api.debank import DebankAPI
import pandas as pd

wallet = '0xbb140caad2a312dcb2d1eaec02bb11b35816d39d'

api = DebankAPI()

balances_df = api.fetch_chain_balances(wallet_address=wallet, dataframe=True, quiet=True)
print(balances_df.head())

tokens_df = api.fetch_token_balances(wallet_address=wallet, dataframe=True)
print(tokens_df.head())

