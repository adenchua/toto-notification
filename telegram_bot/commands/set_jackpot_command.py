from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardRemove,
    Update,
)
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
    CommandHandler,
    CallbackQueryHandler,
)

from shared.logging_helper import logger
from telegram_bot.models.subscriber_model import SubscriberModel
from telegram_bot.singletons import database_service


JACKPOT_THRESHOLD_INPUT = 1


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    keyboard = [
        [InlineKeyboardButton("$2,000,000", callback_data="2000000")],
        [InlineKeyboardButton("$4,000,000", callback_data="4000000")],
        [InlineKeyboardButton("$5,000,000", callback_data="5000000")],
        [InlineKeyboardButton("$8,000,000", callback_data="8000000")],
        [InlineKeyboardButton("$10,000,000", callback_data="10000000")],
    ]

    try:
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "Please select a jackpot threshold. Jackpots equal and above this threshold will be sent to you. Press /cancel anytime to cancel request",
            reply_markup=reply_markup,
        )

        return JACKPOT_THRESHOLD_INPUT
    except Exception as error:
        logger.exception(error)


async def jackpot_threshold_input(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    user_id = str(update.effective_user.id)
    subscriber_model = SubscriberModel(database_service)

    query = update.callback_query
    await query.answer()
    new_jackpot_threshold = int(query.data)

    try:
        subscriber_exist = subscriber_model.check_subscriber_exist(user_id)

        # subscriber doesn't exist, return without doing anything
        if subscriber_exist is False:
            context.user_data.clear()
            return ConversationHandler.END

        subscriber_model.update_subscriber_jackpot_threshold(
            user_id, new_jackpot_threshold
        )
        await query.edit_message_text(
            f"Jackpot threshold updated to {format(new_jackpot_threshold)}"
        )
    except Exception as error:
        logger.exception(error)

    context.user_data.clear()
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Operation cancelled. No jackpot threshold modified",
        reply_markup=ReplyKeyboardRemove(),
    )
    context.user_data.clear()
    return ConversationHandler.END


setjackpot_conv_handler = ConversationHandler(
    entry_points=[CommandHandler("setjackpot", start)],
    states={JACKPOT_THRESHOLD_INPUT: [CallbackQueryHandler(jackpot_threshold_input)]},
    fallbacks=[CommandHandler("cancel", cancel)],
)
