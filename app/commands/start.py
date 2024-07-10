import datetime
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler

# logger
from logger import setup_logger
logger = setup_logger()

from API import get_all_account, get_account_by_id, update_account, delete_account, get_all_transactions, create_transaction, get_transaction, delete_transaction

# Constants for pagination
from configs.app import BUTTONS_PER_PAGE
from functions.str_to_number import convert_to_number

# Define states for ConversationHandler
FROM_ACCOUNT, AMOUNT, AMOUNT_LOW, TO_ACCOUNT = range(4)

def all_accounts(prefix):
    """Send all accounts to the user with a specified prefix for callback_data."""
    accounts = get_all_account().get('accounts')

    if accounts:
         # 按照 "last_update_date" 重新排列账户列表，最新的在前
        sorted_accounts = sorted(accounts, key=lambda x: x['last_update_date'], reverse=True)
        buttons = [InlineKeyboardButton(f"{acc['name']} ({acc['currency']})", callback_data=f"{prefix}_{acc['id']}") for acc in sorted_accounts]
    else:
        buttons = []
    return buttons

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Sends a message with inline buttons attached, with pagination."""
    
    await send_buttons(update.message.chat_id, context, prefix="from_acc")

    return FROM_ACCOUNT


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






async def from_account(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the chosen from account and asks for the amount."""
    query = update.callback_query
    await query.answer()
    context.user_data['from_account'] = query.data.split("_")[2]
    await query.edit_message_text(text="🔴⬆️Please enter the amount to transfer:")
    return AMOUNT

async def amount(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['amount'] = update.message.text
    await update.message.reply_text("🟢⬇️Please enter the transfer in amount: \nif same amount /amount_low_is_same_to_high")
    return AMOUNT_LOW

async def amount_low(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['amount_low'] = update.message.text
    await update.message.reply_text("Please choose the account to transfer to:")
    await send_buttons(update.message.chat_id, context, prefix="to_acc")
    return TO_ACCOUNT

async def amount_low_is_same_to_high(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['amount_low'] = context.user_data['amount']
    await update.message.reply_text("Please choose the account to transfer to:")
    await send_buttons(update.message.chat_id, context, prefix="to_acc")
    return TO_ACCOUNT

async def to_account(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the chosen to account and ends the conversation."""
    query = update.callback_query
    await query.answer()
    context.user_data['to_account'] = query.data.split("_")[2]
    
    from_account = context.user_data['from_account']
    to_account = context.user_data['to_account']
    amount = context.user_data['amount']
    amount_low = context.user_data['amount_low']
    
    

    # add transaction
    datetime_now = datetime.datetime.now()
    amount = convert_to_number(amount)
    amount_low = convert_to_number(amount_low)
    rate = round(amount_low / amount, 6)

    transaction = {
        "serialNumber": 0,
        "account_id_High": from_account,
        "amount_High": amount,
        "rate": rate,
        "amount_Low": amount_low,
        "account_id_Low": to_account,
        "description": None,
        "create_date": datetime_now.isoformat(),
        "last_update_date": datetime_now.isoformat(),
    }

    create_transaction(transaction)

    # Perform the transaction or any other operation
    # await query.edit_message_text(r)

    # - money
    out_money_account = get_account_by_id(from_account)

    new_account_data = {
        'name': out_money_account['name'],
        'currency': out_money_account['currency'],
        'balance': round(out_money_account['balance'] - amount, 6),
        'type': out_money_account['type'],
        'create_date': out_money_account['create_date'],
        'last_update_date': datetime_now.isoformat()
    }

    update_account(account_id=from_account, account_data=new_account_data)


    # + money
    in_money_account = get_account_by_id(to_account)

    new_account_data = {
        'name': in_money_account['name'],
        'currency': in_money_account['currency'],
        'balance': round(in_money_account['balance'] + amount_low, 6),
        'type': in_money_account['type'],
        'create_date': in_money_account['create_date'],
        'last_update_date': datetime_now.isoformat()
    }

    update_account(account_id=to_account, account_data=new_account_data)

    text_out = f"🔴⬆️ {out_money_account['name']}({out_money_account['currency']}): {amount}"
    if rate == 1:
        text_rate = ""
    else:
        text_rate = f"        {out_money_account['currency']}{in_money_account['currency']} rate : {rate}"  + "\n" + f"        {in_money_account['currency']}{out_money_account['currency']} rate : {1/rate}"  + "\n"
    text_in = f"🟢⬇️ {in_money_account['name']}({in_money_account['currency']}): {amount_low}"

    await query.edit_message_text(f"{text_out}\n{text_rate}{text_in}")


    return ConversationHandler.END



async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
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