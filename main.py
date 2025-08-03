import os
import asyncio
import logging
from time import sleep

from dotenv import load_dotenv

from services.database_service import DatabaseService
from services.website_scraper_service import WebsiteScraperService
from scripts.event_download_job import EventDownloadJob

logging.basicConfig(
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
    level=logging.INFO,
)

load_dotenv()

DATABASE_HOST = os.getenv("OPENSEARCH_DATABASE_HOST", "")
DATABASE_USERNAME = os.getenv("OPENSEARCH_DATABASE_USERNAME", "")
DATABASE_PASSWORD = os.getenv("OPENSEARCH_DATABASE_PASSWORD", "")
SCRAPE_TARGET_URL = os.getenv("SCRAPE_TARGET_URL", "")


def check_env_string(key: str, env_string: str | None) -> None:
    """Helper method that logs all empty string environment variables"""
    if env_string == "" or env_string is None:
        logging.warning(f"WARNING: {key} is not defined...")


def check_env():
    """prints a warning for each environment key if it is not defined"""
    check_env_string("DATABASE_HOST", DATABASE_HOST)
    check_env_string("DATABASE_USERNAME", DATABASE_USERNAME)
    check_env_string("DATABASE_PASSWORD", DATABASE_PASSWORD)
    check_env_string("SCRAPE_TARGET_URL", SCRAPE_TARGET_URL)


async def run():
    check_env()
    database_service = DatabaseService(
        host=DATABASE_HOST,
        username=DATABASE_USERNAME,
        password=DATABASE_PASSWORD,
    )
    website_scraper_service = WebsiteScraperService(url=SCRAPE_TARGET_URL)

    SCRAPE_INTERVAL_HOURS = 6
    event_job = EventDownloadJob(
        interval_hours=SCRAPE_INTERVAL_HOURS,
        website_scraper_service=website_scraper_service,
        database_service=database_service,
    )

    task1 = asyncio.create_task(event_job.run())
    await asyncio.wait([task1])


if __name__ == "__main__":
    logging.info("Starting up scripts... Sleeping for 60 seconds...")
    # sleep for 1 minute first on restart to prevent script spam upon startup
    sleep(60 * 1)
    logging.info("Running all background jobs...")
    asyncio.run(run())
