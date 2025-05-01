from vars import API_ID, API_HASH, BOT_TOKEN

# Add imports for environment variables
import os

# Override variables with environment variables if available
API_ID = os.environ.get("API_ID", API_ID)
API_HASH = os.environ.get("API_HASH", API_HASH)
BOT_TOKEN = os.environ.get("BOT_TOKEN", BOT_TOKEN)
LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-1002339598092"))
