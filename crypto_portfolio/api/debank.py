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

class DebankAPI:
    def __init__(self):
        """
        Initialize DebankAPI instance
        API key retrieved from environment variables
        """
        self.api_key = os.getenv("DEBANK_KEY")
        self.base_url = "https://pro-openapi.debank.com"
        self.headers = {
            'accept': 'application/json',
            'AccessKey': self.api_key
        }

    def fetch_interacted_chains(self, wallet_address):
        """
        Fetches list of blockchain networks that a wallet has interacted with.
        Args:
            wallet_address (str): The wallet address to query.
        Returns:
            list: A list of tuples [(chain_id, community_id), ...] where 
                chain_id is the string name of the chain and 
                commmunity_id is the chain's numeric representation
        """
        url = f"{self.base_url}/v1/user/used_chain_list"
        # Call parameters
        params = {'id': wallet_address}
        # Call API
        try:
            response = requests.get(url, headers=self.headers, params=params)
            data = response.json()
            print("Response Structure: ", data)

            # Extract chain ID and community ID with validation
            chains = []
            for chain in data:
                chain_id = chain.get('id', None) # Default to None if not present
                community_id = chain.get('community_id', None) # Default to None if not present

                # Validate data types
                if isinstance(chain_id, str) and (isinstance(community_id, int) or community_id is None):
                    chains.append((chain_id, community_id))
                else:
                    print(f"Skipping invalid entry: {chain}")

            return chains
        except requests.ConnectionError as e:
            print(f"Error fetching interacted chains for {wallet_address}: {e}")
            return []
        
    
if __name__ == "__main__":
    # Try to run fetch_wallets
    print("\nATTEMPTING TO FETCH INTERACTED WALLETS")
    wallet_address = '0x42f50744fabf5e2873bba98234e78b11480fdee8'
    api = DebankAPI()
    chains = api.fetch_interacted_chains(wallet_address)
    print("Fetched chain IDs: ", chains)


            




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