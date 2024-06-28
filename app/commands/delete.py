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

SELECT_ACCOUNT = range(1)

def all_transactions(prefix):
    """Send all transactions to the user with a specified prefix for callback_data."""
    transactions = get_all_transactions().get('transactions')

    if transactions:
        sorted_transactions = sorted(transactions, key=lambda x: x['last_update_date'], reverse=True)
        buttons = [InlineKeyboardButton(f"{transaction['amount_High']} 💲{transaction['rate']} {transaction['amount_Low']} ({transaction['serialNumber']})", callback_data=f"{prefix}_{transaction['serialNumber']}") for transaction in sorted_transactions]
    else:
        buttons = []
    return buttons

async def delete_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    
    await send_buttons(update.message.chat_id, context, prefix="transaction")

    return SELECT_ACCOUNT


async def send_buttons(chat_id, context: ContextTypes.DEFAULT_TYPE, prefix, update_message=None, page=0) -> int:
    """Helper function to send or update buttons with pagination."""
    buttons = all_transactions(prefix)
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


async def select_account(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    query = update.callback_query
    await query.answer()
    serialNumber = int(query.data.split("_")[1])

    transactions = get_all_transactions().get('transactions')

    for transaction in transactions:
        if transaction['serialNumber'] == serialNumber:
            # delete the transaction
            delete_transaction(serialNumber)
            datetime_now = datetime.datetime.now()
            # - money from low
            out_money_account = get_account_by_id(transaction['account_id_Low'])

            new_account_data = {
                'name': out_money_account['name'],
                'currency': out_money_account['currency'],
                'balance': round(out_money_account['balance'] - transaction['amount_Low'], 6),
                'type': out_money_account['type'],
                'create_date': out_money_account['create_date'],
                'last_update_date': datetime_now.isoformat()
            }

            update_account(account_id=transaction['account_id_Low'], account_data=new_account_data)


            # + money to high
            in_money_account = get_account_by_id(transaction['account_id_High'])

            new_account_data = {
                'name': in_money_account['name'],
                'currency': in_money_account['currency'],
                'balance': round(in_money_account['balance'] + transaction['amount_High'], 6),
                'type': in_money_account['type'],
                'create_date': in_money_account['create_date'],
                'last_update_date': datetime_now.isoformat()
            }

            update_account(account_id=transaction['account_id_High'], account_data=new_account_data)

            break
    else:
        await query.edit_message_text("Transaction not found.")
        return ConversationHandler.END


    await query.edit_message_text("Transaction deleted successfully!")


    return ConversationHandler.END


async def cancel_delete(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    await update.message.reply_text('Operation cancelled.')
    return ConversationHandler.END

async def next_page(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Callback function for 'Next' button."""
    query = update.callback_query
    await query.answer()

    current_page = int(query.data.split("_")[2])
    prefix = query.data.split("_")[1]
    await send_buttons(query.message.chat_id, context, prefix=prefix, update_message = query.message ,page=current_page + 1)

    return SELECT_ACCOUNT

async def prev_page(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Callback function for 'Previous' button."""
    query = update.callback_query
    await query.answer()

    current_page = int(query.data.split("_")[2])
    prefix = query.data.split("_")[1]
    await send_buttons(query.message.chat_id, context, prefix=prefix, update_message = query.message ,page=max(0, current_page - 1))

    return SELECT_ACCOUNT