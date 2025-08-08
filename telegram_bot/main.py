from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from telegram_bot.constants import TELEGRAM_BOT_API_TOKEN
from telegram_bot.commands.start_command import start
from telegram_bot.commands.set_jackpot_command import setjackpot_conv_handler

app = ApplicationBuilder().token(TELEGRAM_BOT_API_TOKEN).build()


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Log the error before doing anything else
    print(f"Exception while handling an update: {context.error}")

    # Optionally notify the user or admin
    if update and hasattr(update, "message") and update.message:
        await update.message.reply_text(
            "An unexpected error occurred. Please try again later."
        )


# all available bot commands
app.add_handler(CommandHandler("start", start))
app.add_handler(setjackpot_conv_handler)

# Register the error handler
app.add_error_handler(error_handler)

app.run_polling()
