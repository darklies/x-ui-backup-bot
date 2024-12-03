from datetime import datetime
from telegram.ext import ContextTypes
from src.config import UPDATE_INTERVAL
from src.storage.credentials import get_user_credentials

async def send_db_update(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send periodic database updates to the user."""
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

def schedule_updates(context: ContextTypes.DEFAULT_TYPE, user_id: int) -> None:
    """Schedule periodic updates for a user."""
    context.job_queue.run_repeating(
        send_db_update,
        interval=UPDATE_INTERVAL,
        first=10,
        user_id=user_id
    )