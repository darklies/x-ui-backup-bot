from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler
)
from src.config import BOT_TOKEN
from src.handlers.conversation_states import State
from src.handlers.auth_handler import (
    start,
    get_url,
    get_login,
    get_password,
    cancel
)
from src.handlers.status_handler import status

def main() -> None:
    """Initialize and start the bot."""
    application = Application.builder().token(BOT_TOKEN).build()

    # Set up conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            State.URL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_url)],
            State.LOGIN: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_login)],
            State.PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_password)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    # Add handlers
    application.add_handler(conv_handler)
    application.add_handler(CommandHandler('status', status))

    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()