import inspect

from telegram import Update
from telegram.ext import ContextTypes

from shared.logging_helper import logger
from telegram_bot.models.subscriber_model import SubscriberModel
from telegram_bot.singletons import database_service


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    subscriber_model = SubscriberModel(database_service)
    username = update.effective_user.username
    first_name = update.effective_user.first_name
    last_name = update.effective_user.last_name
    user_id = str(update.effective_user.id)

    reply_message = inspect.cleandoc(
        f"Hello {first_name}! Thank you for showing interest in my project!\n\n"
        f"Please first register your jackpot threshold with the /setjackpot command!\n\n"
    )

    try:
        subscriber_model.create_subscriber(
            subscriber_id=user_id,
            first_name=first_name,
            last_name=last_name,
            username=username,
        )
        await update.message.reply_text(reply_message)
    except Exception as error:
        logger.exception(error)
