import os
import json
import time
from datetime import datetime
import sqlite3
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

# States for conversation
LOGIN, PASSWORD, URL = range(3)

# Store user credentials (in memory - would be better with proper database in production)
user_credentials = {}

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
    
    user_credentials[user_id] = {'url': url}
    await update.message.reply_text("Great! Now send me your username:")
    return LOGIN

async def get_login(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_credentials[user_id]['username'] = update.message.text
    await update.message.reply_text("Now send me your password:")
    return PASSWORD

async def get_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_credentials[user_id]['password'] = update.message.text
    
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
    
    if user_id not in user_credentials:
        return
    
    # Here you would implement the actual X-UI database fetching logic
    # For demonstration, we'll just send a placeholder message
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
    if user_id in user_credentials:
        creds = user_credentials[user_id]
        await update.message.reply_text(
            f"✅ Your X-UI Monitor is active!\n"
            f"URL: {creds['url']}\n"
            f"Username: {creds['username']}\n"
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

def main():
    # Replace 'YOUR_BOT_TOKEN' with your actual bot token from BotFather
    application = Application.builder().token('YOUR_BOT_TOKEN').build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            URL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_url)],
            LOGIN: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_login)],
            PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_password)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    application.add_handler(conv_handler)
    application.add_handler(CommandHandler('status', status))

    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()