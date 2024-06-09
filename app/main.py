import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler

from commands.start import start
from configs.telegram import TOKEN
from error.handler import handler as error_handler

def main() -> None:
    """Start the bot."""
    application = Application.builder().token(TOKEN).build()

    application.add_error_handler(error_handler)

    application.add_handler(CommandHandler("start", start))
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()