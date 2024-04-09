from dotenv import load_dotenv
import os

load_dotenv()

USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
HOST = os.getenv("HOST")
DATABASE = os.getenv("DATABASE")
PORT = os.getenv("PORT")
PAIRS = os.getenv("PAIRS").split(",")
PERCENT = int(os.getenv("PERCENT"))
PERIOD_SEC = int(os.getenv("PERIOD_SEC"))
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
KOEF = int(os.getenv("KOEF"))
