import json
from typing import Dict, Any, Optional
from src.config import CREDENTIALS_FILE

def save_credentials(user_id: int, data: Dict[str, Any]) -> None:
    """Save user credentials to the JSON storage."""
    credentials = load_all_credentials()
    credentials[str(user_id)] = data
    
    with open(CREDENTIALS_FILE, 'w') as f:
        json.dump(credentials, f, indent=2)

def load_all_credentials() -> Dict[str, Dict[str, Any]]:
    """Load all user credentials from storage."""
    try:
        with open(CREDENTIALS_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def get_user_credentials(user_id: int) -> Optional[Dict[str, Any]]:
    """Get credentials for a specific user."""
    credentials = load_all_credentials()
    return credentials.get(str(user_id))