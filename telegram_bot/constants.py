from dotenv import load_dotenv
import os

# load environment keys
load_dotenv()

DATABASE_HOST = os.getenv("OPENSEARCH_DATABASE_HOST", "")
DATABASE_USERNAME = os.getenv("OPENSEARCH_DATABASE_USERNAME", "")
DATABASE_PASSWORD = os.getenv("OPENSEARCH_DATABASE_PASSWORD", "")

TELEGRAM_BOT_API_TOKEN = os.getenv("TELEGRAM_BOT_API_TOKEN", "")
