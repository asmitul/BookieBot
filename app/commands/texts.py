from telegram import Update
from telegram.ext import ContextTypes

from triggers.trigger import Trigger

from send.math import calculate

async def texts(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    msg = update.message.text
    
    t = Trigger(msg)
    
    if t.is_math_expression():
        await calculate(update, context)
    
    
    else:
        # await update.message.reply_text("text")
        pass