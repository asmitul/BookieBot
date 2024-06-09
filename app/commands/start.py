from telegram import Update
from telegram.ext import ContextTypes

# logger
from logger import setup_logger
logger = setup_logger()

from API import get_all_account
    
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    await update.message.reply_text("welcome")

    accounts = get_all_account()

    await update.message.reply_text(accounts)