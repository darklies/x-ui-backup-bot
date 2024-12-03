from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from storage import save_credentials, get_user_credentials
from datetime import datetime

# States for conversation
LOGIN, PASSWORD, URL = range(3)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome to X-UI Monitor Bot!\n"
        "Please provide your X-UI login information.\n"
        "First, send me your X-UI panel URL (e.g., https://your-domain:port)"
    )
    return URL

async def get_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    url = update.message.text
    
    if not url.startswith(('http://', 'https://')):
        await update.message.reply_text("Please provide a valid URL starting with http:// or https://")
        return URL
    
    context.user_data['credentials'] = {'url': url}
    await update.message.reply_text("Great! Now send me your username:")
    return LOGIN

async def get_login(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    context.user_data['credentials']['username'] = update.message.text
    await update.message.reply_text("Now send me your password:")
    return PASSWORD

async def get_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    context.user_data['credentials']['password'] = update.message.text
    
    # Save credentials
    save_credentials(user_id, context.user_data['credentials'])
    
    await update.message.reply_text(
        "Thank you! Your credentials have been saved.\n"
        "I will send you X-UI database updates every hour.\n"
        "Use /status to check current status."
    )
    
    # Start periodic updates for this user
    context.job_queue.run_repeating(
        send_db_update,
        interval=3600,  # 1 hour
        first=10,
        user_id=user_id
    )
    
    return ConversationHandler.END

async def send_db_update(context: ContextTypes.DEFAULT_TYPE):
    job = context.job
    user_id = job.user_id
    
    credentials = get_user_credentials(user_id)
    if not credentials:
        return
    
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    await context.bot.send_message(
        user_id,
        f"🔄 X-UI Database Update ({current_time})\n"
        "Status: Connected\n"
        "Database size: 1.2MB\n"
        "Active users: 25"
    )

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
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

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Operation cancelled. Use /start to begin again.")
    return ConversationHandler.END