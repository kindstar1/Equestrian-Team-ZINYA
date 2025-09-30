import os
from dotenv import load_dotenv

load_dotenv()


TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
DATABASE_URL = os.getenv('DATABASE_URL')
DATABASE_URL_PROD = os.getenv('DATABASE_URL_PROD')

ADMIN_ID = '812366187'

SUPPORT_BOT = '812366187'