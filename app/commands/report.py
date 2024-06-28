import datetime
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler

# logger
from logger import setup_logger
logger = setup_logger()

from API import get_all_account

def buttons():
    buttons = [
        [
            InlineKeyboardButton("Income", callback_data="income"),
            InlineKeyboardButton("Expense", callback_data="expense")
        ],
        [
            InlineKeyboardButton("Liquid", callback_data="liquid"),
            InlineKeyboardButton("Illiquid", callback_data="illiquid")
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


