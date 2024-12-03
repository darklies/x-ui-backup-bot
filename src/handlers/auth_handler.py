from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from src.storage.credentials import save_credentials
from src.handlers.conversation_states import State
from src.services.update_service import schedule_updates

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start the conversation and ask for URL."""
    await update.message.reply_text(
        "Welcome to X-UI Monitor Bot!\n"
        "Please provide your X-UI login information.\n"
        "First, send me your X-UI panel URL (e.g., https://your-domain:port)"
    )
    return State.URL

async def get_url(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle URL input and ask for username."""
    url = update.message.text
    
    if not url.startswith(('http://', 'https://')):
        await update.message.reply_text("Please provide a valid URL starting with http:// or https://")
        return State.URL
    
    context.user_data['credentials'] = {'url': url}
    await update.message.reply_text("Great! Now send me your username:")
    return State.LOGIN

async def get_login(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle username input and ask for password."""
    context.user_data['credentials']['username'] = update.message.text
    await update.message.reply_text("Now send me your password:")
    return State.PASSWORD

async def get_password(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle password input and complete setup."""
    user_id = update.message.from_user.id
    context.user_data['credentials']['password'] = update.message.text
    
    save_credentials(user_id, context.user_data['credentials'])
    
    await update.message.reply_text(
        "Thank you! Your credentials have been saved.\n"
        "I will send you X-UI database updates every hour.\n"
        "Use /status to check current status."
    )
    
    schedule_updates(context, user_id)
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancel the conversation."""
    await update.message.reply_text("Operation cancelled. Use /start to begin again.")
    return ConversationHandler.END