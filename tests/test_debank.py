from crypto_portfolio.api.debank import DebankAPI

wallet = '0xbb140caad2a312dcb2d1eaec02bb11b35816d39d'

api = DebankAPI()

tokens_df = api.fetch_token_balances(wallet_address=wallet, dataframe=True, quiet=True)



