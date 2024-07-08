from datetime import datetime, timedelta, timezone
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler

# logger
from logger import setup_logger
logger = setup_logger()

from API import get_all_account, get_all_transactions, get_account_by_id

def buttons():
    buttons = [
        [
            InlineKeyboardButton("Income", callback_data="income"),
            InlineKeyboardButton("Expense", callback_data="expense")
        ],
        [
            InlineKeyboardButton("Last Month", callback_data="last_month"),
            InlineKeyboardButton("This Month", callback_data="this_month")
        ],
        [
            InlineKeyboardButton("Liquid", callback_data="liquid"),
            InlineKeyboardButton("Illiquid", callback_data="illiquid")
        ],
        [
            InlineKeyboardButton("Vadeli", callback_data="vadeli")
        ]
    ]

    return buttons

async def report(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    
    reply_markup = InlineKeyboardMarkup(buttons())
    # send message
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Please choose", reply_markup=reply_markup, parse_mode="MarkdownV2")


async def callback_income(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    data = get_all_account()

    list_type_0 = []

    for account in data['accounts']:
        currency = account['currency']
        balance = account['balance']
        if account['type'] == 0:
            list_type_0.append(f"{currency} : {balance}")

    currency_totals = {}

    for item in list_type_0:
        currency, balance = item.split(' : ')
        balance = float(balance)
        if currency in currency_totals:
            currency_totals[currency] += balance
        else:
            currency_totals[currency] = balance

    # round 2 decimal
    result = [f'{currency} \: `{round(total, 2)}`' for currency, total in currency_totals.items()]

    await context.bot.send_message(chat_id=update.effective_chat.id, text="\n".join(result), parse_mode="MarkdownV2")

async def callback_expense(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    data = get_all_account()

    list_type_2 = []

    for account in data['accounts']:
        currency = account['currency']
        balance = account['balance']
        if account['type'] == 2:
            list_type_2.append(f"{currency} : {balance}")

    currency_totals = {}

    for item in list_type_2:
        currency, balance = item.split(' : ')
        balance = float(balance)
        if currency in currency_totals:
            currency_totals[currency] += balance
        else:
            currency_totals[currency] = balance

    # round 2 decimal
    result = [f'{currency} \: `{round(total, 2)}`' for currency, total in currency_totals.items()]

    await context.bot.send_message(chat_id=update.effective_chat.id, text="\n".join(result), parse_mode="MarkdownV2")

async def callback_liquid(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    data = get_all_account()

    list_type_1 = []

    for account in data['accounts']:
        currency = account['currency']
        balance = account['balance']
        if account['type'] == 1:
            list_type_1.append(f"{currency} : {balance}")

    currency_totals = {}

    for item in list_type_1:
        currency, balance = item.split(' : ')
        balance = float(balance)
        if currency in currency_totals:
            currency_totals[currency] += balance
        else:
            currency_totals[currency] = balance

    # round 2 decimal
    result = [f'{currency} \: `{round(total, 2)}`' for currency, total in currency_totals.items()]

    await context.bot.send_message(chat_id=update.effective_chat.id, text="\n".join(result), parse_mode="MarkdownV2")


async def callback_illiquid(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    data = get_all_account()

    list_type_11 = []

    for account in data['accounts']:
        currency = account['currency']
        balance = account['balance']
        if account['type'] == 11:
            list_type_11.append(f"{currency} : {balance}")

    currency_totals = {}

    for item in list_type_11:
        currency, balance = item.split(' : ')
        balance = float(balance)
        if currency in currency_totals:
            currency_totals[currency] += balance
        else:
            currency_totals[currency] = balance

    # round 2 decimal
    result = [f'{currency} \: `{round(total, 2)}`' for currency, total in currency_totals.items()]

    try:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="\n".join(result), parse_mode="MarkdownV2")
    except Exception as e:
        logger.error(e)



async def callback_last_month(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Fetch all transactions
    transactions = get_all_transactions()
    transactions = transactions.get('transactions')

    # List to store transactions from last month
    serialNumber_last_month = []

    # Dictionary to store the sum of amount_Low for each account_id_Low
    account_low_sums = {}

    # Get current time
    current_time = datetime.now()

    # Get first and last day of last month
    first_day_of_current_month = current_time.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    last_day_of_last_month = first_day_of_current_month - timedelta(seconds=1)
    first_day_of_last_month = last_day_of_last_month.replace(day=1)

    for transaction in transactions:
        iso_time_str = transaction['create_date']
        parsed_time = datetime.fromisoformat(iso_time_str)

        if first_day_of_last_month <= parsed_time <= last_day_of_last_month:
            serialNumber_last_month.append(transaction['serialNumber'])
            
            account_id_low = transaction['account_id_Low']
            amount_low = transaction['amount_Low']

            if account_id_low in account_low_sums:
                account_low_sums[account_id_low] += amount_low
            else:
                account_low_sums[account_id_low] = amount_low

    # 
    last_month_account_cost = {}
    for account_id_low, amount_low in account_low_sums.items():
        account = get_account_by_id(account_id_low)

        if account.get("type") == 2:
            data = {
                "name": account.get("name"),
                "currency": account.get("currency"),
                "cost": round(amount_low, 6)
            }

            last_month_account_cost[account_id_low] = data

    # sort by cost
    sorted_data = dict(sorted(last_month_account_cost.items(), key=lambda item: item[1]['cost'], reverse=True))

    # for loop . send every message 
    for account_id_low, data in sorted_data.items():
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{data['name']} : {data['cost']}")



async def callback_this_month(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Fetch all transactions
    transactions = get_all_transactions()
    transactions = transactions.get('transactions')

    # List to store transactions from last month
    serialNumber_this_month = []

    # Dictionary to store the sum of amount_Low for each account_id_Low
    account_low_sums = {}

    # Get current time
    current_time = datetime.now()

    # Get first and last day of last month
    first_day_of_current_month = current_time.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    

    for transaction in transactions:
        iso_time_str = transaction['create_date']
        parsed_time = datetime.fromisoformat(iso_time_str)

        if first_day_of_current_month <= parsed_time:
            serialNumber_this_month.append(transaction['serialNumber'])
            
            account_id_low = transaction['account_id_Low']
            amount_low = transaction['amount_Low']

            if account_id_low in account_low_sums:
                account_low_sums[account_id_low] += amount_low
            else:
                account_low_sums[account_id_low] = amount_low
    print(f"serialNumber_this_month : {serialNumber_this_month}")
    # 
    last_month_account_cost = {}
    for account_id_low, amount_low in account_low_sums.items():
        account = get_account_by_id(account_id_low)

        if account.get("type") == 2:
            data = {
                "name": account.get("name"),
                "currency": account.get("currency"),
                "cost": round(amount_low, 6)
            }

            last_month_account_cost[account_id_low] = data

    # sort by cost
    sorted_data = dict(sorted(last_month_account_cost.items(), key=lambda item: item[1]['cost'], reverse=True))

    # for loop . send every message 
    for account_id_low, data in sorted_data.items():
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{data['name']} : {data['cost']}")


async def callback_vadeli(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    accounts = get_all_account()
    accounts = accounts.get('accounts')

    # Get current time
    current_time = datetime.now()

    # Get first and last day of last month
    yesterday = current_time - timedelta(days=1)


    for account in accounts:
        iso_time_str = account['create_date']
        parsed_time = datetime.fromisoformat(iso_time_str)

        if yesterday <= parsed_time :
            # YYYY-MM-DD
            date_str = parsed_time.strftime("%Y-%m-%d")
            name = account['name'] + " - " + account['currency']
            balance = account['balance']

            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{date_str} \n{name} : {balance}")
