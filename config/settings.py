import os
from dotenv import load_dotenv

class Settings:
    def load_api_key(self):
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("API key not found in .env file")
        return api_key
