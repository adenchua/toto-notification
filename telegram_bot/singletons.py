from shared.database_service import DatabaseService
from telegram_bot.constants import DATABASE_HOST, DATABASE_PASSWORD, DATABASE_USERNAME

database_service = DatabaseService(
    host=DATABASE_HOST, password=DATABASE_PASSWORD, username=DATABASE_USERNAME
)
