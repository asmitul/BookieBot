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

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raises HTTPError if the response status is 4xx, 5xx
        return response.json()  # Assuming the response is a JSON array of account dictionaries
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return []  # Return an empty list or handle the error as needed                             


def create_account(account_data: Dict[str, str]) -> Dict[str, str]:
    url = f"http://{host}:{port}/{VERSION}/accounts/"
    headers = {
        "accept": "application/json",
        "access_token": API_KEY,
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, headers=headers, json=account_data)
        response.raise_for_status()  # Raises HTTPError if the response status is 4xx, 5xx
        return response.json()  # Assuming the response is a JSON object
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return {}  # Return an empty dictionary or handle the error as needed

def get_account_by_id(account_id: str) -> Dict[str, str]:
    url = f"http://{host}:{port}/{VERSION}/accounts/{account_id}"
    headers = {
        "accept": "application/json",
        "access_token": API_KEY
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raises HTTPError if the response status is 4xx, 5xx
        return response.json()  # Assuming the response is a JSON object
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return {}  # Return an empty dictionary or handle the error as needed


def update_account(account_id: str, account_data: Dict[str, str]) -> Dict[str, str]:
    url = f"http://{host}:{port}/{VERSION}/accounts/{account_id}"
    headers = {
        "accept": "application/json",
        "access_token": API_KEY,
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.put(url, headers=headers, json=account_data)
        response.raise_for_status()  # Raises HTTPError if the response status is 4xx, 5xx
        return response.json()  # Assuming the response is a JSON object
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return {}  # Return an empty dictionary or handle the error as needed


def delete_account(account_id: str) -> Dict[str, str]:
    url = f"http://{host}:{port}/{VERSION}/accounts/{account_id}"
    headers = {
        "accept": "application/json",
        "access_token": API_KEY
    }
    
    try:
        response = requests.delete(url, headers=headers)
        response.raise_for_status()  # Raises HTTPError if the response status is 4xx, 5xx
        return response.json()  # Assuming the response contains a JSON object with the success message
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return {"success": False, "message": str(e)}  # Return an error message



def get_all_transactions() -> List[Dict[str, str]]:
    url = f"http://{host}:{port}/{VERSION}/transactions/"
    headers = {
        "accept": "application/json",
        "access_token": API_KEY
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raises HTTPError if the response status is 4xx, 5xx
        return response.json()  # Assuming the response is a JSON array of transaction dictionaries
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return []  # Return an empty list or handle the error as needed
    

def create_transaction(transaction_data: dict) -> dict:
    url = f"http://{host}:{port}/{VERSION}/transactions/"
    headers = {
        "accept": "application/json",
        "access_token": API_KEY,
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, headers=headers, json=transaction_data)
        response.raise_for_status()  # Raises HTTPError if the response status is 4xx, 5xx
        return response.json()  # Assuming the response is a JSON object
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return {}  # Return an empty dict or handle the error as needed
    

def get_transaction(transaction_id: str) -> dict:
    url = f"http://{host}:{port}/{VERSION}/transactions/{transaction_id}"
    headers = {
        "accept": "application/json",
        "access_token": API_KEY
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raises HTTPError if the response status is 4xx, 5xx
        return response.json()  # Assuming the response is a JSON object
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return {}  # Return an empty dict or handle the error as needed
    

def delete_transaction(transaction_id: int) -> dict:
    url = f"http://{host}:{port}/{VERSION}/transactions/{transaction_id}"
    headers = {
        "accept": "application/json",
        "access_token": API_KEY
    }
    
    try:
        response = requests.delete(url, headers=headers)
        response.raise_for_status()  # Raises HTTPError if the response status is 4xx, 5xx
        return response.json()  # Assuming the response is a JSON object
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return {"success": False, "message": "An error occurred while deleting the transaction"}  # Return a default error message or handle the error as needed