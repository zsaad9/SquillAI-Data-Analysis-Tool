import os
from dotenv import load_dotenv

load_dotenv()

# Configuration file for environment variables
class Config:
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
