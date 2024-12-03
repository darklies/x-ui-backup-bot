import json
import os
from typing import Dict, Any
from config import CREDENTIALS_FILE

def save_credentials(user_id: int, data: Dict[str, Any]) -> None:
    credentials = load_all_credentials()
    credentials[str(user_id)] = data
    
    with open(CREDENTIALS_FILE, 'w') as f:
        json.dump(credentials, f, indent=2)

def load_all_credentials() -> Dict[str, Dict[str, Any]]:
    if not os.path.exists(CREDENTIALS_FILE):
        return {}
    
    try:
        with open(CREDENTIALS_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}

def get_user_credentials(user_id: int) -> Dict[str, Any]:
    credentials = load_all_credentials()
    return credentials.get(str(user_id), {})