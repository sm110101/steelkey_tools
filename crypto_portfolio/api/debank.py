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
        self.api_key = os.getenv("DEBANK_KEY")
        self.base_url = "https://pro-openapi.debank.com"
        self.headers = {
            'accept': 'application/json',
            'AccessKey': self.api_key
        }

    def fetch_interacted_chains(self, wallet_address):
        url = f"{self.base_url}/v1/user/used_chain_list"
        # Call parameters
        params = {
            'id': wallet_address
        }
        # Call API
        response = requests.get(url, headers=self.headers, params=params)
        data = response.json()
        # Extract chain IDs
        chain_ids = [chain['id'] for chain in data]
        return chain_ids


    def fetch_chain_balances(self, chain_id, wallet_address):
        url = f"{self.base_url}/v1/user/chain_balance"
        # Call parameters
        params = {
            'chain_id': chain_id
        }

    def fetch_interacted_chains(self, address):
        url = f"{self.base_url}/v1/user/interacted_chains?user_address={address}"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = requests.get(url, headers=headers)
        return response.json()
