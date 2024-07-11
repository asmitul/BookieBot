from datetime import datetime, timedelta, timezone
import html
from telegram.constants import ParseMode
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler
from API import get_fon_current_price

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
            InlineKeyboardButton("Last Week", callback_data="last_week"),
            InlineKeyboardButton("This Week", callback_data="this_week")
        ],
        [
            InlineKeyboardButton("Liquid", callback_data="liquid"),
            InlineKeyboardButton("Illiquid", callback_data="illiquid")
        ],
        [
            InlineKeyboardButton("Fon", callback_data="fon"),
            InlineKeyboardButton("Vadeli", callback_data="vadeli"),
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


async def callback_last_week(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Fetch all transactions
    transactions = get_all_transactions()
    transactions = transactions.get('transactions')

    # List to store transactions from last week
    serialNumber_last_week = []

    # Dictionary to store the sum of amount_Low for each account_id_Low
    account_low_sums = {}

    # Get current time
    current_time = datetime.now()

    # Get first and last day of last week
    first_day_of_current_week = current_time - timedelta(days=current_time.weekday())
    first_day_of_current_week = first_day_of_current_week.replace(hour=0, minute=0, second=0, microsecond=0)
    last_day_of_last_week = first_day_of_current_week - timedelta(seconds=1)
    first_day_of_last_week = first_day_of_current_week - timedelta(days=7)

    for transaction in transactions:
        iso_time_str = transaction['create_date']
        parsed_time = datetime.fromisoformat(iso_time_str)

        if first_day_of_last_week <= parsed_time <= last_day_of_last_week:
            serialNumber_last_week.append(transaction['serialNumber'])
            
            account_id_low = transaction['account_id_Low']
            amount_low = transaction['amount_Low']

            if account_id_low in account_low_sums:
                account_low_sums[account_id_low] += amount_low
            else:
                account_low_sums[account_id_low] = amount_low

    # 
    last_week_account_cost = {}
    for account_id_low, amount_low in account_low_sums.items():
        account = get_account_by_id(account_id_low)

        if account.get("type") == 2:
            data = {
                "name": account.get("name"),
                "currency": account.get("currency"),
                "cost": round(amount_low, 6)
            }

            last_week_account_cost[account_id_low] = data

    # sort by cost
    sorted_data = dict(sorted(last_week_account_cost.items(), key=lambda item: item[1]['cost'], reverse=True))

    # for loop . send every message
    first_day_of_last_week = first_day_of_last_week.strftime("%Y-%m-%d %H:%M")
    last_day_of_last_week = last_day_of_last_week.strftime("%Y-%m-%d %H:%M")

    text = f"{first_day_of_last_week} <-> {last_day_of_last_week} \n\n"
    for account_id_low, data in sorted_data.items():
        text += f"{data['name']} : {data['cost']}\n"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)

async def callback_this_week(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Fetch all transactions
    transactions = get_all_transactions()
    transactions = transactions.get('transactions')

    # List to store transactions from last week
    serialNumber_this_week = []

    # Dictionary to store the sum of amount_Low for each account_id_Low
    account_low_sums = {}

    # Get current time
    current_time = datetime.now()

    # Get first day 00:00 of this week
    first_day_of_current_week = current_time - timedelta(days=current_time.weekday())
    first_day_of_current_week = first_day_of_current_week.replace(hour=0, minute=0, second=0, microsecond=0)    

    for transaction in transactions:
        iso_time_str = transaction['create_date']
        parsed_time = datetime.fromisoformat(iso_time_str)

        if first_day_of_current_week <= parsed_time:
            serialNumber_this_week.append(transaction['serialNumber'])
            
            account_id_low = transaction['account_id_Low']
            amount_low = transaction['amount_Low']

            if account_id_low in account_low_sums:
                account_low_sums[account_id_low] += amount_low
            else:
                account_low_sums[account_id_low] = amount_low
    # 
    last_week_account_cost = {}
    for account_id_low, amount_low in account_low_sums.items():
        account = get_account_by_id(account_id_low)

        if account.get("type") == 2:
            data = {
                "name": account.get("name"),
                "currency": account.get("currency"),
                "cost": round(amount_low, 6)
            }

            last_week_account_cost[account_id_low] = data

    # sort by cost
    sorted_data = dict(sorted(last_week_account_cost.items(), key=lambda item: item[1]['cost'], reverse=True))

    # for loop . send every message 
    # convert current_time to YYYY-MM-DD
    current_time = current_time.strftime("%Y-%m-%d %H:%M")
    first_day_of_current_week = first_day_of_current_week.strftime("%Y-%m-%d %H:%M")
    text = f"{first_day_of_current_week} <-> {current_time} \n\n"
    for account_id_low, data in sorted_data.items():
        text += f"{data['name']} : {data['cost']} \n"
        
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)



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

async def callback_fon(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    accounts = get_all_account()
    accounts = accounts.get('accounts')

    transactions = get_all_transactions()
    transactions = transactions.get('transactions')

    # resort transactions by serialNumber high to low
    transactions.sort(key=lambda x: x['serialNumber'], reverse=True)

    fon = []

    for account in accounts:
        if account['type'] == 4:
            if account['balance'] > 0:
                account_id = account['id']
                amount = account['balance']                

                for transaction in transactions:
                    data = {}
                    if transaction['account_id_Low'] == account_id:
                        if amount <= 0 :
                            break
                        else:
                            diff = amount - transaction['amount_Low']

                            if diff <= 0:
                                data['serialNumber'] = transaction['serialNumber']
                                data['account_id'] = account['id']
                                data['name'] = account['name']
                                data['price'] = transaction['amount_High'] / transaction['amount_Low']
                                data['amount'] = amount

                                fon.append(data)
                                amount = 0

                            else:
                                data['serialNumber'] = transaction['serialNumber']
                                data['account_id'] = account['id']
                                data['name'] = account['name']
                                data['price'] = transaction['amount_High'] / transaction['amount_Low']
                                data['amount'] = transaction['amount_Low']

                                fon.append(data)
                                amount = amount - transaction['amount_Low']
    
    # print(f"fon : {fon}")
    # [{'serialNumber': 126, 'account_id': '668cf37656b883407f082f1b', 'name': "IHK İŞ'TE KADIN", 'rate': 13.1, 'amount': 10.0}, {'serialNumber': 123, 'account_id': '668cf37656b883407f082f1b', 'name': "IHK İŞ'TE KADIN", 'rate': 13.0, 'amount': 30.0}, {'serialNumber': 127, 'account_id': '668e423343426f64b88634d3', 'name': 'TEE fon', 'rate': 20.0, 'amount': 10.0}]            
            
    for data in fon:
        # get name and rate
        name = data['name']
        price = round(data['price'], 6)
        amount = data['amount']
        
        fon_code = name.split()[0]
        current_price = get_fon_current_price(fon_code)
        # replace , to .
        try:
            current_price = current_price.replace(",", ".")
        except:
            pass
        # convert to float or int
        current_price = convert_to_num(current_price)

        diff = round((current_price - price) * amount, 2)

        if diff > 0:
            text = f"<pre language='python'>{html.escape(str(fon_code))} = {html.escape(str(amount))} * ({html.escape(str(current_price))} - {html.escape(str(price))}) # 🟢{html.escape(str(diff))} TL</pre>"
        else:
            text = f"<pre language='python'>{html.escape(str(fon_code))} = {html.escape(str(amount))} * ({html.escape(str(current_price))} - {html.escape(str(price))}) # 🔴{html.escape(str(diff))} TL</pre>"

        await context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode=ParseMode.HTML)
            
            
        
def convert_to_num(s: str):
    try:
        # Try converting to an integer
        return int(s)
    except ValueError:
        try:
            # If it fails, try converting to a float
            return float(s)
        except ValueError:
            # If both conversions fail, return None or raise an error
            return None
