from asyncio import sleep
import sys

from toto_service.models.event_model import EventModel
from toto_service.models.subscriber_model import SubscriberModel
from toto_service.services.notification_service import NotificationService
from shared.database_service import DatabaseService
from shared.logging_helper import logger


class SubscriberNotificationJob:
    def __init__(
        self,
        interval_hours: int,
        database_service: DatabaseService,
    ):
        self.interval_hours = interval_hours
        self.database_service = database_service
        self.notification_service = NotificationService()

    async def run(self) -> None:
        event_model = EventModel(database_service=self.database_service)
        subscriber_model = SubscriberModel(database_service=self.database_service)

        while True:
            try:
                logger.info("Notifying subscribers...")
                event = event_model.get_latest_event()
                subscribers = subscriber_model.get_active_subscribers()

                # no event exist in db
                if event is None:
                    return

                jackpot: int = event.get("jackpot", None)
                next_draw_datestring: str = event.get("next_draw_datestring", None)

                if jackpot is None or next_draw_datestring is None:
                    raise Exception("There is something wrong with the latest event")

                for subscriber in subscribers:
                    subscriber_jackpot_threshold: int = subscriber.get(
                        "jackpot_threshold", sys.maxsize
                    )
                    subscriber_last_notified_event: str = subscriber.get(
                        "last_notified_event", None
                    )
                    subscriber_id: str = subscriber.get("_id", None)

                    is_jackpot_above_threshold: bool = (
                        jackpot >= subscriber_jackpot_threshold
                    )
                    is_new_event: bool = (
                        subscriber_last_notified_event != next_draw_datestring
                    )

                    # new event with jackpot above set threshold, send message
                    # and update subscriber event last_notified_event
                    if is_jackpot_above_threshold and is_new_event:
                        subscriber_model.update_subscriber_event(
                            subscriber_id=subscriber_id, draw_event=next_draw_datestring
                        )
                        await self.__send_message(
                            jackpot=jackpot,
                            draw_info=next_draw_datestring,
                            subscriber_id=subscriber_id,
                        )

            except Exception as error:
                logger.exception(error)
            finally:
                logger.info(
                    f"Background job completed! Sleeping for {self.interval_hours} hours..."
                )

                # sleep for the x number of hours before restarting the crawl
                await sleep(60 * 60 * self.interval_hours)

    async def __send_message(
        self, jackpot: int, subscriber_id: str, draw_info: str
    ) -> None:
        jackpot_message = f"${format(jackpot, ",")}"
        message = f"The next jackpot {jackpot_message} will be drawn on {draw_info}. Good luck!"
        await self.notification_service.send_message(
            message=message, receiver_chat_id=subscriber_id
        )
