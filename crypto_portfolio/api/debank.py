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
- Look at using /total_balance for getting chain balances
- Add chain_name to cache
- Fix issues with price retrieval
- Add dataframe creation to fetch_token_balances
"""

# Function execution timer
def timing_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time

        # Check if quiet parameter exists and is False
        if not kwargs.get('quiet', False):
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

        # Store cached chain ID and community ID
        self.cached_chains = None
        # Retrieve API key and define url/headers
        self.api_key = os.getenv("DEBANK_KEY")
        self.base_url = "https://pro-openapi.debank.com"
        self.headers = {
            'accept': 'application/json',
            'AccessKey': self.api_key
        }

    @timing_decorator
    def fetch_interacted_chains(self, wallet_address, quiet=False):
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
            if not quiet:
                print('fetching interacted chains...')
            response = requests.get(url, headers=self.headers, params=params)
            data = response.json()

            # Extract chain ID and community ID with validation
            chains = []
            for chain in data:
                chain_name = chain.get('name', None) # Default to None if not present
                chain_id = chain.get('id', None) # Default to None if not present
                chain_community_id = chain.get('community_id', None) # Default to None if not present

                # Cache chain_id and chain_community_id
                if chain_id and chain_community_id:
                    self.cached_chains = self.cached_chains or []
                    self.cached_chains.append((chain_id, chain_community_id))

                chains.append((chain_name, chain_id, chain_community_id))

            return chains
        
        except requests.ConnectionError as e:
            print(f"Error fetching interacted chains for {wallet_address}: {e}")

            return []
        
    @timing_decorator
    def fetch_chain_balances(self, wallet_address, dataframe=False, quiet=False):
        """
        Fetches the USD balance of a given wallet by chain_id
        Args: 
            wallet_address (str): user's wallet address.
        Returns:
            dictionary: a dictionary representing chain balances {chain_id: {chain_name, chain_community_id, $balance}}
            DataFrame: a Pandas dataframe if dataframe=True with columns ['chain_id', 'chain_name', 'chain_community_id', 'usd_balance']
         """
        url = f"{self.base_url}/v1/user/chain_balance"
        # Get interacted chains (including chain names, so cache is not necessary here)
        chains_tuple = self.fetch_interacted_chains(wallet_address)

        # Initialize empty dictionary to store balances
        chain_balances = {}
        # unpack tuple to get chain IDs
        if not quiet:
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
                        'chain_name': chain_name,
                        'chain_community_id': chain_community_id,
                        'usd_balance': usd_value
                    }
                    chain_balances[chain_id] = chain_info

            except requests.ConnectionError as e:
                print(f"Error extracting chain balances for {chain_id}: {e}")
                return None
            
        if dataframe:
            # Convert nested dictionary into DataFrame
            df = pd.DataFrame.from_dict(chain_balances, orient='index')
            # Reset Index to make chain_id a column
            df.reset_index(inplace=True)
            # Rename cols
            df.columns = ['chain_id', 'chain_name', 'chain_community_id', 'usd_balance']

            return df
    
        return chain_balances
    
    # Helper method to get cached chain IDs
    def get_cached_ids(self, wallet_address):
        """
        Returns cached chain IDs or fetches them if not cached
        Args:
            wallet_address (str): User's wallet address
        Returns:
            list: List of chain IDs where total USD balance on chain > $1
        """
        if self.cached_chains is None:
            # If not cached, run fetch_chain_balances to cache
            self.fetch_interacted_chains(wallet_address, quiet=True)
        return self.cached_chains

    @timing_decorator
    def fetch_token_balances(self, wallet_address, dataframe=False, quiet=False):
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
        id_and_cid = self.get_cached_ids(wallet_address)

        # Initialize dictionary to store token balances
        token_balances = {}

        # unpack tuple to get chain_id call paramter
        for chain_id, chain_community_id in id_and_cid:
            # Initialize empty list for this chan 
            token_balances[chain_id] = []
            # Define call parameters
            params = {
                'id': wallet_address,
                'chain_id': chain_id
            }
            
            # Print chain_id for each run 
            if not quiet:
                print(f"fetching {chain_id} balances...")

            # Call
            try:
                response = requests.get(url, headers=self.headers, params=params)
                data = response.json()

                # Gather relevant info
                for token in data:
                    # Attach info to subdictionary
                    info = {
                        'token_name': token.get('name', None),
                        'token_id': token.get('id', None),
                        'token_decimals': token.get('decimals', None),
                        'token_quantity': token.get('amount', 0),
                    }

                    token_balances[chain_id].append(info)

            except requests.ConnectionError as e:
                print(f"Error retrieving token balance info for {chain_id}: {e}")
                return None

        return token_balances

        
def temp_toDF(dict):
    df = pd.DataFrame.from_dict(dict, orient="index")
    df.reset_index(inplace=True)
    return df


if __name__ == "__main__":
    # Try to run fetch_wallets
    wallet_address = '0xbb140caad2a312dcb2d1eaec02bb11b35816d39d'
    api = DebankAPI()
    #chain_balances = api.fetch_chain_balances(wallet_address)
    #print('\nCHAIN BALACES DICT\n')
    #pprint(chain_balances)
    #print('\nCHAIN BALANCES DF\n')
    #print(temp_toDF(chain_balances))
    print('\nToken Balances\n')
    pprint(api.fetch_token_balances(wallet_address))




            


