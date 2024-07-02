from dotenv import load_dotenv
import os

load_dotenv(dotenv_path='env/.env')

def get_openai_key():
    return os.getenv("OPENAI_API_KEY_ACM")

def get_claud_key():
    return os.getenv("CLAUD_API_KEY_ACM")