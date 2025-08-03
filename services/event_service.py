from .database_service import DatabaseService
from utils.date_utils import current_datetime_iso


class EventService:
    def __init__(self, database_service: DatabaseService):
        self.database_service = database_service
        self.index_name = "draw-event"

    def create_event(self, jackpot: int, event_datestring: str):
        """
        Creates a draw event in the database
        """
        id = event_datestring
        document = {
            "jackpot": jackpot,
            "next_draw_datestring": event_datestring,
            "crawl_date": current_datetime_iso(),
        }
        self.database_service.ingest_document(self.index_name, document, id)
