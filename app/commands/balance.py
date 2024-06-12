import datetime
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler
from telegram.helpers import escape_markdown

# logger
from logger import setup_logger
logger = setup_logger()

from API import get_all_account, get_account_by_id

# Constants for pagination
from configs.app import BUTTONS_PER_PAGE
from functions.str_to_number import convert_to_number

# Define states for ConversationHandler
ACCOUNT_BALANCE = range(1)

def all_accounts(prefix):
    """Send all accounts to the user with a specified prefix for callback_data."""
    accounts = get_all_account().get('accounts')

    if accounts:
        buttons = [InlineKeyboardButton(f"{acc['name']} ({acc['currency']})", callback_data=f"{prefix}_{acc['id']}") for acc in accounts]
    else:
        buttons = []
    return buttons

async def balance_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Sends a message with inline buttons attached, with pagination."""
    
    await send_buttons(update.message.chat_id, context, prefix="acc_balance")

    return ACCOUNT_BALANCE


async def send_buttons(chat_id, context: ContextTypes.DEFAULT_TYPE, prefix, update_message=None, page=0) -> int:
    """Helper function to send or update buttons with pagination."""
    buttons = all_accounts(prefix)
    start_index = page * BUTTONS_PER_PAGE
    end_index = min(len(buttons), (page + 1) * BUTTONS_PER_PAGE)

    keyboard = [
        buttons[i:i + 2] for i in range(start_index, end_index, 2)
    ]
    
    pagination_buttons = []
    if page > 0:
        pagination_buttons.append(InlineKeyboardButton("Previous", callback_data=f"prev_{prefix}_{page}"))
    if end_index < len(buttons):
        pagination_buttons.append(InlineKeyboardButton("Next", callback_data=f"next_{prefix}_{page}"))

    keyboard.append(pagination_buttons)

    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update_message:
        await update_message.edit_reply_markup(reply_markup)
    else:
        await context.bot.send_message(chat_id, "Please choose:", reply_markup=reply_markup)

    return start_index, end_index






async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the chosen from account and asks for the amount."""
    query = update.callback_query
    await query.answer()
    account_id = query.data.split("_")[2]

    r = get_account_by_id(account_id=account_id)
    r = escape_markdown(text=r['name'], version=2) + " : " +"`" + str(round(r['balance'], 6)) + "`" + " " + r['currency']
    await query.edit_message_text(r, parse_mode="MarkdownV2")
    
    return ConversationHandler.END





async def cancel_balance(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    await update.message.reply_text('Operation cancelled.')
    return ConversationHandler.END

async def next_page3(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Callback function for 'Next' button."""
    query = update.callback_query
    await query.answer()

    current_page = int(query.data.split("_")[3])
    prefix = query.data.split("_")[1] + "_" + query.data.split("_")[2] 
    await send_buttons(query.message.chat_id, context, prefix=prefix, update_message = query.message ,page=current_page + 1)

    return ACCOUNT_BALANCE

async def prev_page3(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Callback function for 'Previous' button."""
    query = update.callback_query
    await query.answer()

    current_page = int(query.data.split("_")[3])
    prefix = query.data.split("_")[1] + "_" + query.data.split("_")[2] 
    await send_buttons(query.message.chat_id, context, prefix=prefix, update_message = query.message ,page=max(0, current_page - 1))

    return ACCOUNT_BALANCE