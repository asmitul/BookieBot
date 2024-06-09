import time
from typing import Dict, List
import requests
from configs.server import SERVER_HOST as host, SERVER_PORT as port, API_KEY
VERSION = "v1"


def get_all_account() -> List[Dict[str, str]]:
    url = f"http://{host}:{port}/{VERSION}/accounts"
    headers = {
        "accept": "application/json",
        "access_token": API_KEY
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()  # Assuming the response is a JSON array of account dictionaries
    else:
        response.raise_for_status()

if __name__ == "__main__":
    print(get_all_account())