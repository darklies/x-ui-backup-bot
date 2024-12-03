from telegram import Update
from telegram.ext import ContextTypes
from src.storage.credentials import get_user_credentials

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the status command."""
    user_id = update.message.from_user.id
    credentials = get_user_credentials(user_id)
    
    if credentials:
        await update.message.reply_text(
            f"✅ Your X-UI Monitor is active!\n"
            f"URL: {credentials['url']}\n"
            f"Username: {credentials['username']}\n"
            "Updates: Every 1 hour"
        )
    else:
        await update.message.reply_text(
            "❌ No monitoring configured.\n"
            "Use /start to set up X-UI monitoring."
        )