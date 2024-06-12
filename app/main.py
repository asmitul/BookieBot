from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, filters

from commands.start import start, from_account, amount, amount_low, to_account, cancel, next_page, prev_page,next_page2, prev_page2,FROM_ACCOUNT, AMOUNT, AMOUNT_LOW, TO_ACCOUNT
from commands.create import create, account_name, currency, cancel_create,ACCOUNT_NAME, CURRENCY
from commands.balance import balance_start, balance, ACCOUNT_BALANCE, cancel_balance, next_page3, prev_page3
from configs.telegram import TOKEN
from error.handler import handler as error_handler
from commands.texts import texts as text_handler

def main() -> None:
    """Start the bot."""
    application = Application.builder().token(TOKEN).build()

    application.add_error_handler(error_handler)
    
    # start command handler
    start_conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            FROM_ACCOUNT: [CallbackQueryHandler(from_account, pattern=r"^from_acc_.+$"),CallbackQueryHandler(next_page, pattern=r'^next_from_acc_\d+$'),CallbackQueryHandler(prev_page, pattern=r'^prev_from_acc_\d+$')],
            AMOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, amount)],
            AMOUNT_LOW: [MessageHandler(filters.TEXT & ~filters.COMMAND, amount_low)],
            TO_ACCOUNT: [CallbackQueryHandler(to_account, pattern=r"^to_acc_.+$"),CallbackQueryHandler(next_page2, pattern=r'^next_to_acc_\d+$'),CallbackQueryHandler(prev_page2, pattern=r'^prev_to_acc_\d+$')],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    application.add_handler(start_conversation_handler)

    # create
    create_conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('create', create)],
        states={
            ACCOUNT_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, account_name)],
            CURRENCY: [MessageHandler(filters.TEXT & ~filters.COMMAND, currency)],
        },
        fallbacks=[CommandHandler('cancel_create', cancel_create)],
    )

    application.add_handler(create_conversation_handler)

    # balance
    get_balance_conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('balance', balance_start)],
        states={
            ACCOUNT_BALANCE: [CallbackQueryHandler(balance, pattern=r"^acc_balance_.+$"),CallbackQueryHandler(next_page3, pattern=r'^next_acc_balance_\d+$'),CallbackQueryHandler(prev_page3, pattern=r'^prev_acc_balance_\d+$')],
        },
        fallbacks=[CommandHandler('cancel_balance', cancel_balance)],
    )

    application.add_handler(get_balance_conversation_handler)

    application.add_handler(MessageHandler(filters.TEXT, text_handler))

    
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()