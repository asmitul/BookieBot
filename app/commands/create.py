import datetime
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler

# logger
from logger import setup_logger
logger = setup_logger()

from API import create_account

ACCOUNT_NAME, CURRENCY, TYPE = range(3)


async def create(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Please enter the name of the account:")
    return ACCOUNT_NAME

async def account_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    account_name = update.message.text
    context.user_data['account_name'] = account_name
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Please enter the type of the account , \n0 for income \n1 for Liquid assets like cash / banck account \n11 for Illiquid assets, \n2 for expense:")
    return TYPE

async def type(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    type = update.message.text
    context.user_data['type'] = type
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Please enter the currency of the account:")
    return CURRENCY

async def currency(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    currency = update.message.text
    context.user_data['currency'] = currency

    await context.bot.send_message(chat_id=update.effective_chat.id, text="Please wait while we create your account...")

    datetime_now = datetime.datetime.now()

    account = {
        'name': context.user_data['account_name'],
        'currency': context.user_data['currency'],
        'balance': 0,
        'type': context.user_data['type'],
        'create_date': datetime_now.isoformat(),
        'last_update_date': datetime_now.isoformat()
    }

    create_account(account)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Account created successfully!")
    return ConversationHandler.END

async def cancel_create(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    print("cancel start")
    """Cancels and ends the conversation."""
    await update.message.reply_text('Operation cancelled.')
    return ConversationHandler.END