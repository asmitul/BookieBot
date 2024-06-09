import json
import os


if 'SERVER_ENV' in os.environ and os.environ['SERVER_ENV'] == 'production':
    SERVER_HOST = os.environ["SERVER_HOST"]
    SERVER_PORT = os.environ["SERVER_PORT"]
    API_KEY = os.environ["API_KEY"]

else:
    with open("config.dev.json", 'r') as f:
        config = json.load(f)
    SERVER_HOST = config["server"]["host"]
    SERVER_PORT = config["server"]["port"]
    API_KEY = config["server"]["api_key"]