import os
from typing import Final

# Bot configuration
BOT_TOKEN: Final = 'YOUR_BOT_TOKEN'

# Update intervals (in seconds)
UPDATE_INTERVAL: Final = 3600  # 1 hour

# Storage configuration
DATA_DIR: Final = os.path.join(os.path.dirname(__file__), '..', 'data')
CREDENTIALS_FILE: Final = os.path.join(DATA_DIR, 'credentials.json')

# Create data directory if it doesn't exist
os.makedirs(DATA_DIR, exist_ok=True)