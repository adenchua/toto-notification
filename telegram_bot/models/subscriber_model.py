from shared.database_service import DatabaseService
from shared.date_utils import current_datetime_iso


class SubscriberModel:
    def __init__(self, database_service: DatabaseService):
        self.database_service = database_service
        self.index_name = "subscriber"

    def create_subscriber(
        self, subscriber_id: str, username: str, first_name: str, last_name: str
    ) -> None:
        """
        Creates a new subscriber in the database
        """
        document = {
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            "registered_date": current_datetime_iso(),
        }

        # subscriber already exists, do not create subscriber
        if self.check_subscriber_exist(subscriber_id):
            return

        subscribers = self.database_service.ingest_document(
            index=self.index_name, document=document, id=subscriber_id
        )
        return subscribers

    def check_subscriber_exist(self, subscriber_id: str) -> bool:
        """
        Checks if a subscriber exists in the database
        Returns a boolean value
        """
        result = self.database_service.fetch_document_by_id(
            self.index_name, document_id=subscriber_id
        )

        return result != None

    def update_subscriber_jackpot_threshold(
        self, subscriber_id: str, jackpot_threshold: int
    ) -> None:
        """
        Updates a subscriber jackpot threshold
        """
        updated_fields = {"jackpot_threshold": jackpot_threshold}
        self.database_service.update_document(
            index=self.index_name,
            document_id=subscriber_id,
            updated_fields=updated_fields,
        )
