import json
import os


if 'SERVER_ENV' in os.environ and os.environ['SERVER_ENV'] == 'production':
    TOKEN = os.environ['TELEGRAM_TOKEN']

    with open("config.json", 'r') as f:
        config = json.load(f)
    DEVELOPER_ID = config["telegram"]["developer_id"]

else:
    with open("config.dev.json", 'r') as f:
        config = json.load(f)
    TOKEN = config["telegram"]["bot_token"]
    DEVELOPER_ID = config["telegram"]["developer_id"]
