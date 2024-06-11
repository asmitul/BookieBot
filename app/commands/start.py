from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler

# logger
from logger import setup_logger
logger = setup_logger()

from API import get_all_account, get_account_by_id, update_account, delete_account, get_all_transactions, create_transaction, get_transaction, delete_transaction

# Constants for pagination
from configs.app import BUTTONS_PER_PAGE

# Define states for ConversationHandler
FROM_ACCOUNT, AMOUNT, RATE, TO_ACCOUNT = range(4)

def all_accounts(prefix):
    print("all_accounts start")
    """Send all accounts to the user with a specified prefix for callback_data."""
    accounts = get_all_account().get('accounts')
    print(f"all_accounts: {accounts}")
    if accounts:
        buttons = [InlineKeyboardButton(f"{acc['name']} ({acc['currency']})", callback_data=f"{prefix}_{acc['id']}") for acc in accounts]
    else:
        buttons = []
    print("all_accounts end")
    return buttons

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    print("start start")
    """Sends a message with inline buttons attached, with pagination."""
    
    await send_buttons(update.message.chat_id, context, prefix="from_acc")

    print("start end")
    return FROM_ACCOUNT


async def send_buttons(chat_id, context: ContextTypes.DEFAULT_TYPE, prefix, update_message=None, page=0) -> int:
    print(f" prefix: {prefix}")
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
    
    print(f"update_message 111111111111 :{update_message}")
    if update_message:
        await update_message.edit_reply_markup(reply_markup)
    else:
        await context.bot.send_message(chat_id, "Please choose:", reply_markup=reply_markup)

    return start_index, end_index






async def from_account(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    print("from_account start")
    """Stores the chosen from account and asks for the amount."""
    query = update.callback_query
    await query.answer()
    context.user_data['from_account'] = query.data.split("_")[2]
    await query.edit_message_text(text="Please enter the amount to transfer:")
    return AMOUNT

async def amount(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    print("amount start")
    """Stores the amount and asks for the exchange rate."""
    context.user_data['amount'] = update.message.text
    await update.message.reply_text("Please enter the exchange rate:")
    return RATE

async def rate(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    print("rate start")
    """Stores the exchange rate and asks the user to choose the to account."""
    context.user_data['rate'] = update.message.text
    await update.message.reply_text("Please choose the account to transfer to:")
    await send_buttons(update.message.chat_id, context, prefix="to_acc")
    return TO_ACCOUNT

async def to_account(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    print("to_account start")
    """Stores the chosen to account and ends the conversation."""
    query = update.callback_query
    await query.answer()
    context.user_data['to_account'] = query.data.split("_")[2]
    
    from_account = context.user_data['from_account']
    to_account = context.user_data['to_account']
    amount = context.user_data['amount']
    rate = context.user_data['rate']
    
    # Perform the transaction or any other operation
    await query.edit_message_text(
        text=f"Transfer from account {from_account} to account {to_account} with amount {amount} and rate {rate}."
    )
    return ConversationHandler.END



async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    print("cancel start")
    """Cancels and ends the conversation."""
    await update.message.reply_text('Operation cancelled.')
    return ConversationHandler.END

async def next_page(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Callback function for 'Next' button."""
    query = update.callback_query
    await query.answer()

    current_page = int(query.data.split("_")[3])
    prefix = query.data.split("_")[1] + "_" + query.data.split("_")[2] 
    await send_buttons(query.message.chat_id, context, prefix=prefix, update_message = query.message ,page=current_page + 1)

    return FROM_ACCOUNT

async def prev_page(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Callback function for 'Previous' button."""
    query = update.callback_query
    await query.answer()

    current_page = int(query.data.split("_")[3])
    prefix = query.data.split("_")[1] + "_" + query.data.split("_")[2] 
    await send_buttons(query.message.chat_id, context, prefix=prefix, update_message = query.message ,page=max(0, current_page - 1))

    return FROM_ACCOUNT

async def next_page2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Callback function for 'Next' button."""
    query = update.callback_query
    await query.answer()

    current_page = int(query.data.split("_")[3])
    prefix = query.data.split("_")[1] + "_" + query.data.split("_")[2] 
    print(f"next page prefix: {prefix}")
    await send_buttons(query.message.chat_id, context, prefix=prefix, update_message = query.message ,page=current_page + 1)

    return TO_ACCOUNT

async def prev_page2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Callback function for 'Previous' button."""
    query = update.callback_query
    await query.answer()

    current_page = int(query.data.split("_")[3])
    prefix = query.data.split("_")[1] + "_" + query.data.split("_")[2] 
    await send_buttons(query.message.chat_id, context, prefix=prefix, update_message = query.message ,page=max(0, current_page - 1))

    return TO_ACCOUNT