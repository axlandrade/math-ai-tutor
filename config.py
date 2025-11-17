from dotenv import load_dotenv
import os

load_dotenv()  # carrega o arquivo .env

API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME = "gpt-4.1-nano"
