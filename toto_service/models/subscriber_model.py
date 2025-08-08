from shared.database_service import DatabaseService


class SubscriberModel:
    def __init__(self, database_service: DatabaseService):
        self.database_service = database_service
        self.index_name = "subscriber"

    def get_active_subscribers(self) -> list[dict]:
        """
        Retrieves all active subscribers from the database.
        An active subscribe is someone who has a jackpot_threshold set
        """
        query_body = {
            "size": 10000,
            "query": {"exists": {"field": "jackpot_threshold"}},
        }
        subscribers = self.database_service.fetch_documents(
            index=self.index_name, query_body=query_body
        )
        return subscribers

    def update_subscriber_event(self, subscriber_id: str, draw_event: str) -> None:
        updated_fields = {"last_notified_event": draw_event}
        self.database_service.update_document(
            index=self.index_name,
            document_id=subscriber_id,
            updated_fields=updated_fields,
        )
