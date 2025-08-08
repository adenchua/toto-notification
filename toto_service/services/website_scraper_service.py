import re

import requests
from bs4 import BeautifulSoup


class WebsiteScraperService:
    def __init__(self, url: str):
        self.url = url

    def __scrape_html_content(self) -> BeautifulSoup:
        """
        Scrapes the website to retrieve the next draw details
        """
        url = self.url
        headers = {"User-Agent": "Mozilla/5.0"}

        response = requests.get(url, headers=headers)
        result = BeautifulSoup(response.text, "html.parser")
        return result

    def __parse_jackpot(self, jackpot_text: str) -> int:
        """
        Cleans the jackpot string content and converts to int
        """
        found_dollar_sign = jackpot_text.find("$")
        found_est = jackpot_text.find("est")

        if found_dollar_sign == -1 or found_est == -1:
            raise Exception(f"Jackpot element malformed: '{jackpot_text}'")

        # \D matches any non-digit, replace with empty string
        jackpot_number_string = re.sub(r"\D", "", jackpot_text)

        return int(jackpot_number_string)

    def __parse_draw_date(self, draw_date_text: str) -> str:
        """
        Stub created to parse the draw date. Currently, return the text as it is
        """
        return draw_date_text

    def get_next_estimate(self) -> dict:
        """
        Retrieves the jackpot and next draw date from the website
        """
        content = self.__scrape_html_content()

        next_jackpot = content.find("span").text
        next_draw_date = content.find(class_="toto-draw-date").text

        return {
            "jackpot": self.__parse_jackpot(next_jackpot),
            "next_draw_date": self.__parse_draw_date(next_draw_date),
        }
