import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    DEBANK_API_KEY = os.getenv("DEBANK_KEY")
    BASE_URL = "https://pro-openapi.debank.com"