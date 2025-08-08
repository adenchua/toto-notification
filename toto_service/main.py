import asyncio
from time import sleep

from toto_service.services.website_scraper_service import WebsiteScraperService
from toto_service.jobs.event_download_job import EventDownloadJob
from toto_service.jobs.subscriber_notification_job import SubscriberNotificationJob
from toto_service.constants import (
    DATABASE_HOST,
    DATABASE_PASSWORD,
    DATABASE_USERNAME,
    SCRAPE_TARGET_URL,
    WEBSITE_SCRAPING_INTERVAL_HOURS,
    SUBSCRIBER_NOTIFICATION_INTERVAL_HOURS,
)
from shared.database_service import DatabaseService
from shared.logging_helper import logger


async def run():
    database_service = DatabaseService(
        host=DATABASE_HOST,
        username=DATABASE_USERNAME,
        password=DATABASE_PASSWORD,
    )
    website_scraper_service = WebsiteScraperService(url=SCRAPE_TARGET_URL)

    event_job = EventDownloadJob(
        interval_hours=WEBSITE_SCRAPING_INTERVAL_HOURS,
        website_scraper_service=website_scraper_service,
        database_service=database_service,
    )

    notification_job = SubscriberNotificationJob(
        interval_hours=SUBSCRIBER_NOTIFICATION_INTERVAL_HOURS,
        database_service=database_service,
    )

    task1 = asyncio.create_task(event_job.run())
    task2 = asyncio.create_task(notification_job.run())

    await asyncio.wait([task2])


if __name__ == "__main__":
    logger.info("Starting up scripts... Sleeping for 60 seconds...")
    # sleep for 1 minute first on restart to prevent script spam upon startup
    sleep(60 * 1)
    logger.info("Running all background jobs...")
    asyncio.run(run())
