import telegram

from toto_service.constants import TELEGRAM_BOT_API_TOKEN


class NotificationService:
    def __init__(self):
        self.bot = telegram.Bot(token=TELEGRAM_BOT_API_TOKEN)

    def __format_telegram_string(self, string: str) -> str:
        """
        Telegram message formatting is different from telegram bot API message syntax
        This function formats telegram format syntax to telegram bot api message syntax
        """
        string = string.replace("**", "*")  # bold word
        string = string.replace("__", "_")  # italic
        return string

    async def send_message(self, message: str, receiver_chat_id: str):
        """
        sends a message to the client through the Telegram bot
        """
        formatted_message = self.__format_telegram_string(message)
        await self.bot.send_message(
            chat_id=receiver_chat_id,
            text=formatted_message,
        )
