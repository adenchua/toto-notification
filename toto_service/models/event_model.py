from datetime import datetime
from zoneinfo import ZoneInfo

from shared.database_service import DatabaseService
from shared.date_utils import current_datetime_iso


class EventModel:
    def __init__(self, database_service: DatabaseService):
        self.database_service = database_service
        self.index_name = "draw-event"

    def __parse_datestring(self, datestring: str) -> str:
        date_string_clean = datestring.replace(" , ", ", ")

        date_format = "%a, %d %b %Y, %I.%M%p"

        # Parse to naive datetime
        dt_naive = datetime.strptime(date_string_clean, date_format)
        dt_gmt8 = dt_naive.replace(tzinfo=ZoneInfo("Asia/Singapore"))

        return dt_gmt8.isoformat()

    def create_event(self, jackpot: int, event_datestring: str):
        """
        Creates a draw event in the database
        """
        id = event_datestring
        parsed_date_string = self.__parse_datestring(event_datestring)
        document = {
            "jackpot": jackpot,
            "next_draw_datestring": event_datestring,
            "crawl_date": current_datetime_iso(),
            "draw_date": parsed_date_string,
        }
        self.database_service.ingest_document(self.index_name, document, id)

    def get_latest_event(self) -> dict | None:
        """
        Retrieves the latest event from the database by the crawl_date.
        If there are no events, returns None
        """
        query_body = {
            "size": 1,
            "sort": [{"crawl_date": {"order": "desc"}}],
            "query": {"match_all": {}},
        }
        result = self.database_service.fetch_documents(
            index=self.index_name, query_body=query_body
        )

        if len(result) == 0:
            return None

        return result[0]
