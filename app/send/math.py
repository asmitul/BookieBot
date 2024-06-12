from telegram import Update
from telegram.ext import ContextTypes

# logger
from logger import setup_logger
logger = setup_logger()

async def calculate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text
    s = msg.rstrip()
    if "*" in s or "/" in s or "+" in s or "-" in s:
        try:
            r = "`" + str(round(eval(s), 2)) + "`"
            await update.message.reply_text(r, parse_mode="MarkdownV2")
        except (SyntaxError, NameError, TypeError, ZeroDivisionError , ValueError, AttributeError, IndexError, KeyError, NotImplementedError) as e:
            logger.error(f"An error occurred while calculating: {str(e)}")