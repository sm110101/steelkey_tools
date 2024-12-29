# Key Storage
import os
from dotenv import load_dotenv, dotenv_values
# API
import requests
import time
import json
# Data
import pandas as pd
import numpy as np
# Timing decorator
from functools import wraps
# Pretty print for temp dev tooling
from pprint import pprint


"""
TO DO
- Test with different wallet addresses
"""

# Function execution timer
def timing_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"{func.__name__}: {execution_time:.2f} seconds\n")
        return result
    return wrapper


class DebankAPI:
    def __init__(self):
        """
        Initialize DebankAPI instance
        API key retrieved from environment variables
        """
        # load environment variables
        load_dotenv()

        # Retrieve API key and define url/headers
        self.api_key = os.getenv("DEBANK_KEY")
        self.base_url = "https://pro-openapi.debank.com"
        self.headers = {
            'accept': 'application/json',
            'AccessKey': self.api_key
        }

    @timing_decorator
    def fetch_interacted_chains(self, wallet_address):
        """
        Fetches list of blockchain networks that a wallet has interacted with.
        Args:
            wallet_address (str): The wallet address to query.
        Returns:
            list: A list of tuples [(chain_id, community_id, chain_name), ...] where 
                chain_id is the abbreviated string name of the chain and 
                commmunity_id is the chain's numeric representation
                chain_name is the full name of chain
        """
        url = f"{self.base_url}/v1/user/used_chain_list"
        # Call parameters
        params = {'id': wallet_address}
        # Call API
        try:
            response = requests.get(url, headers=self.headers, params=params)
            data = response.json()

            # Extract chain ID and community ID with validation
            chains = []
            for chain in data:
                chain_name = chain.get('name', None) # Default to None if not present
                chain_id = chain.get('id', None) # Default to None if not present
                chain_community_id = chain.get('community_id', None) # Default to None if not present
                
                chains.append((chain_name, chain_id, chain_community_id))


            return chains
        except requests.ConnectionError as e:
            print(f"Error fetching interacted chains for {wallet_address}: {e}")
            return []
        
    @timing_decorator
    def fetch_chain_balances(self, wallet_address, dataframe = False):
        """
        Fetches the USD balance of a given wallet by chain_id
        Args: 
            wallet_address (str): user's wallet address.
        Returns:
            dictionary: a dictionary of pairs representing chain balances {chain: $balance}
         """
        url = f"{self.base_url}/v1/user/chain_balance"
        # Get interacted chains
        print("fetching interacted chains...")
        chains_tuple = self.fetch_interacted_chains(wallet_address)

        # Initialize empty dictionary to store balances
        chain_balances = {}
        # unpack tuple to get chain IDs
        print("fetching chain balances...")
        for chain_name, chain_id, chain_community_id in chains_tuple:
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
                        'chain_id': chain_id,
                        'chain_community_id': chain_community_id,
                        'usd_balance': usd_value
                    }
                    chain_balances[chain_name] = chain_info

            except requests.ConnectionError as e:
                print(f"Error extracting chain balances for {chain_id}: {e}")
                return None
            
        if dataframe:
            # Convert nested dictionary into DataFrame
            df = pd.DataFrame.from_dict(chain_balances, orient='index')
            # Reset Index to make chain_name a column
            df.reset_index(inplace=True)
            # Rename cols
            df.columns = ['chain_name', 'chain_id', 'chain_community_id', 'usd_balance']

            return df
    
        return chain_balances
    
        
    
if __name__ == "__main__":
    # Try to run fetch_wallets
    wallet_address = '0x42f50744fabf5e2873bba98234e78b11480fdee8'
    api = DebankAPI()
    chain_balances_df = api.fetch_chain_balances(wallet_address, dataframe=True)
    print('\nCHAIN BALACES\n')
    print(chain_balances_df.sort_values(by=))




            




    #def fetch_chain_balances(self, wallet_address):
    #    url = f"{self.base_url}/v1/user/chain_balance"
    #    # Fetch chain IDs
    #    chain_ids = self.fetch_interacted_chains(wallet_address)
    #    for chain_id in chain_ids:
    #        params = {
    #            'chain_id': chain_id,
    #            'id': wallet_address
    #        }
    #        # Call API
    #        response = requests.get(url, headers=self.headers, params=params)
    #        data = response.json()
    #        print(data)
#
    #    # Call parameters
    #    params = {
    #        'chain_id': chain_id
    #    }
#
    #def fetch_interacted_chains(self, address):
    #    url = f"{self.base_url}/v1/user/interacted_chains?user_address={address}"
    #    headers = {"Authorization": f"Bearer {self.api_key}"}
    #    response = requests.get(url, headers=headers)
    #    return response.json()
#