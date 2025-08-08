from asyncio import sleep

from toto_service.services.website_scraper_service import WebsiteScraperService
from toto_service.models.event_model import EventModel
from shared.database_service import DatabaseService
from shared.logging_helper import logger


class EventDownloadJob:
    def __init__(
        self,
        interval_hours: int,
        website_scraper_service: WebsiteScraperService,
        database_service: DatabaseService,
    ):
        self.interval_hours = interval_hours
        self.website_scraper_service = website_scraper_service
        self.event_model = EventModel(database_service)

    async def run(self) -> None:
        while True:
            try:
                logger.info("Scraping website to obtain next event...")
                event = self.website_scraper_service.get_next_estimate()
                jackpot = event.get("jackpot", 0)
                next_draw_datestring = event.get("next_draw_date", None)
                self.event_model.create_event(jackpot, next_draw_datestring)

            except Exception as error:
                logger.exception(error)
            finally:
                logger.info(
                    f"Background job completed! Sleeping for {self.interval_hours} hours..."
                )

                # sleep for the x number of hours before restarting the crawl
                await sleep(60 * 60 * self.interval_hours)
