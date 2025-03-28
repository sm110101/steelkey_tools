import requests
import json
import pandas as pd
import numpy as np
# Pretty print for temp dev tooling
from pprint import pprint
import gc
from crypto_portfolio.config import Config
from crypto_portfolio.utils import timing_decorator


class DebankBalances:
    def __init__(self):
        """
        Initialize DebankAPI instance
        API key retrieved from environment variables
        """
        # Store cached wallet chain_ids and token_ids
        self.cache = {}

        # Retrieve API key and define url/headers
        self.api_key = Config.DEBANK_API_KEY
        self.base_url = Config.BASE_URL
        self.headers = {
            'accept': 'application/json',
            'AccessKey': self.api_key
        }

    def clear_cache(self):
        """
        Clears the cached chain data (self.cached_chains) to free memory
        Should be called when cache is no longer needed or before processing new data
        """
        self.cache = {}
        gc.collect()


    @timing_decorator
    def fetch_interacted_chains(self, wallet_address, output=False, quiet=True):
        """
        Fetches list of blockchain networks that a wallet has interacted with.
        defaults to no output, unless user wants to extract interacted chains only
        Args:
            wallet_address (str): The wallet address to query.
        Returns:
            list: A list [chain_id,...] where 
                chain_id is the abbreviated string name of the chain 
        """
        url = f"{self.base_url}/v1/user/used_chain_list"
        # Call parameters
        params = {'id': wallet_address}
        # Call API
        try:
            if quiet==False:
                print('fetching interacted chains...')
            response = requests.get(url, headers=self.headers, params=params)
            data = response.json()

            # Extract chain ID and community ID with validation
            for chain in data:
                chain_name = chain.get('name') 
                chain_id = chain.get('id') 
                chain_community_id = chain.get('community_id') 

                # Cache chain_id and chain_community_id
                if chain_id and chain_community_id:
                    if chain_id not in self.cache:
                        self.cache[chain_id] = {
                            'chain_name': chain_name,
                            'chain_community_id': chain_community_id,
                            'tokens': {}
                        }

                chains = list(self.cache.keys())

            del data
            if output:
                return chains

        except requests.ConnectionError as e:
            print(f"Error fetching interacted chains for {wallet_address}: {e}")
    

    # def fetch_tokens & cache
    @timing_decorator
    def fetch_chain_balances(self, wallet_address, dataframe=False, quiet=True):
        """
        Fetches the USD balance of a given wallet by chain_id
        Args: 
            wallet_address (str): user's wallet address.
        Returns:
            dictionary: a dictionary representing chain balances {chain_id: {chain_name, chain_community_id, $balance}}
            DataFrame: a Pandas dataframe if dataframe=True with columns ['chain_id', 'usd_balance']
         """
        url = f"{self.base_url}/v1/user/chain_balance"
        # Get interacted chains 
        if not self.cache:
            self.fetch_interacted_chains(wallet_address, quiet=True)

        # Initialize empty dictionary to store balances
        chain_balances = {}
        # unpack tuple to get chain IDs
        if quiet==False:
            print("fetching chain balances...")

        for chain_id in self.cache:
            params = {
                'id': wallet_address,
                'chain_id': chain_id
            }

            # Call 
            try:
                response = requests.get(url, headers=self.headers, params=params)
                data = response.json()

                # Extract balances for only $1+ chains
                usd_value = round(data.get('usd_value', 0), 4)
                if usd_value > 1:
                    chain_info = {
                        'usd_balance': usd_value
                    }
                    chain_balances[chain_id] = chain_info
                
                # Del data after processing
                del data

            except requests.ConnectionError as e:
                print(f"Error extracting chain balances for {chain_id}: {e}")
                return None
            
        if dataframe:
            if chain_balances:
                # Convert nested dictionary into DataFrame
                df = pd.DataFrame.from_dict(chain_balances, orient='index')
                # Reset Index to make chain_id a column
                df.reset_index(inplace=True)
                df.columns = ['chain_id', 'usd_balance']
                return df
            else:
                print("Debug: chain balances is empty. Returning an empty DataFrame.")
                return pd.DataFrame(columns=['chain_id', 'balance_usd'])

        return chain_balances



    @timing_decorator
    def fetch_token_balances(self, wallet_address, dataframe=False, quiet=True):
        """
        Fetches the quantity, id, and name of tokens by chain, by wallet address
        Args:
            wallet_address (str): User's wallet address
        Returns:
            dictionary: A dictionary containing token holdings info
            DataFrame: (id dataframe=True) A Pandas Dataframe containing token holdings info
        """
        url = f"{self.base_url}/v1/user/token_list"
        # Get interacted chains from cache
        if not self.cache:
            self.fetch_interacted_chains(wallet_address, quiet=True)

        for chain_id in self.cache:
            params = {
                'id': wallet_address,
                'chain_id': chain_id
            }

            try:
                if quiet==False:
                    print(f"Fetching tokens for chain {chain_id}...")

                # Call
                response = requests.get(url, headers=self.headers, params=params)
                data = response.json()

                # Gather token info (excluding price)
                for token in data:
                    is_core = token['is_core']
                    if is_core:
                        token_id = token['id']
                        token_info = {
                            'token_name': token.get('name'),
                            'token_id': token_id,
                            'token_quantity': token.get('amount'),
                            'token_price': token.get('price')
                        }
                        
                        self.cache[chain_id]['tokens'][token_id] = token_info

                del data

            except requests.ConnectionError as e:
                print(f"Error fetching tokens for chain {chain_id}: {e}")
                return None
            
        if dataframe:
            records = []
            for chain_id, chain_data in self.cache.items():
                for token_id, token_data in chain_data['tokens'].items():
                    records.append({
                        'chain_id': chain_id,
                        'chain_name': chain_data['chain_name'],
                        'chain_community_id': chain_data['chain_community_id'],
                        **token_data
                    })
            
            df = pd.DataFrame(records)
            df['usd_balance'] = df['token_quantity'] * df['token_price']
            return df
        
        return self.cache
    
    @timing_decorator
    def fetch_interacted_protocols(self, wallet_address, dataframe=False, quiet=True)

    


if __name__ == "__main__":
    # Try to run fetch_wallets
    wallet_address = '0xbb140caad2a312dcb2d1eaec02bb11b35816d39d'
    api = DebankBalances()
    #chain_balances = api.fetch_chain_balances(wallet_address)
    print(api.fetch_token_balances(wallet_address, dataframe=True, quiet=True))

    #print("Fetching Interacted Chains...")
    #api.fetch_interacted_chains(wallet_address, quiet=False)
    #print("Cache after fetching interacted chains\n")
    #pprint(api.cache)
#
    #print("Fetching Chain Balances...")
    #api.fetch_chain_balances(wallet_address, quiet=True)
    #print("cache after fetching chain balances\n")
    #pprint(api.cache)
#
    #print("Fetching token balances")
    #api.fetch_token_balances(wallet_address, quiet=True)
    #print("cache after fetching token balances\n")
    #pprint(api.cache)
#
    #print("Clearing Cache")
    #api.clear_cache()
    #print("Cache after clearing\n")
    #pprint(api.cache)
#