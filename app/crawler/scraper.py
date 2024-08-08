import time
import pathlib
import os
import re
from typing import Optional

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import (
    presence_of_all_elements_located)
from selenium.common.exceptions import NoSuchElementException
from selectolax.parser import HTMLParser

from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent

from app.utilities import MatchData
from app.logger import logger


MAIN_URL = "https://www.flashscore.com/"


EVENT_CONTAINER = "div.sportName"
EVENT_MORE = "a.event__more"

ua = UserAgent()
current_path = pathlib.Path(os.getcwd())
driver_path = current_path / 'chromedriver' / 'chromedriver.exe'


class ScrapingBot:
    def __init__(self, wait_time, timeout):
        ua = UserAgent()
        chrome_options = Options()
        chrome_options.add_argument(f"user-agent={ua.random}")
        chrome_options.add_argument("--start-maximized")

        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )
        self.wait_time = wait_time
        self.timeout = timeout
        logger.info(f"{type(self).__name__} successfully init")

    def scroll_to_end(self) -> None:
        last_height = self.driver.execute_script(
            "return document.body.scrollHeight"
            )
        while True:
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
                )
            time.sleep(1)
            new_height = self.driver.execute_script(
                "return document.body.scrollHeight"
                )
            if new_height == last_height:
                break
            last_height = new_height
        logger.info("scroll to end")

    def quit(self) -> None:
        self.driver.quit()
        logger.info("The driver has been quit")

    def get_page(self, url: str, css_selector: Optional[str] = None):
        self.driver.get(url)
        if css_selector:
            WebDriverWait(self.driver, self.timeout).until(
                presence_of_all_elements_located((By.CSS_SELECTOR,
                                                  css_selector))
            )
        time.sleep(self.wait_time)
        logger.info(f"{url}\nhas been openned")

    def click_element(self, css_selector: str):
        self.driver.find_element(By.CSS_SELECTOR, css_selector).click()
        time.sleep(self.wait_time)

    def parse_league_page(self, league_url: str) -> list:
        self.get_page(MAIN_URL+league_url, EVENT_CONTAINER)
        self.scroll_to_end()

        while True:
            try:
                event_more_elem = self.driver.find_element(By.CSS_SELECTOR,
                                                           EVENT_MORE)
            except NoSuchElementException:
                event_more_elem = None
            if event_more_elem:
                event_more_elem.click()
                self.scroll_to_end()
            else:
                break

        event_links = []
        html_nodes = HTMLParser(self.driver.page_source).css(
            "div.sportName > div.event__match"
            )
        for node in html_nodes:
            event_links.append(node.css_first("[href]").attrs.get('href'))
        return event_links

    def parse_archive(self, archive_url):
        self.get_page(archive_url, "section.archive")
        self.scroll_to_end()

        result = []
        html_nodes = HTMLParser(self.driver.page_source).css(
            "section.archive > div.archive__row"
        )
        for node in html_nodes:
            result.append(node.css_first("[href]").attrs.get('href'))
        return result

    def parse_match(self, match_link: str) -> Optional[MatchData]:
        stats_css = ("div.filterOver>div:first-child>"
                     "a[href*='match-statistics']")
        self.get_page(match_link, stats_css)
        self.driver.find_element(By.CSS_SELECTOR, stats_css).click()
        self.scroll_to_end()
        html = HTMLParser(self.driver.page_source)

        _duel_info = html.css_first("div.duelParticipant")
        _match_status = _duel_info.css_first("div[class*='score']"
                                             ).last_child.last_child.text()
        logger.info(f"{_match_status}")
        if _match_status.lower() == 'finished':
            league, round_num = html.css_first(
                "span.tournamentHeader__country"
                ).css_first("a").text().split(' - ', 1)
            start_time = _duel_info.css_first("div[class*='startTime']"
                                              ).child.text()
            team_home = _duel_info.css_first("div[class*='home']"
                                             ).last_child.css_first("a").text()
            team_away = _duel_info.css_first("div[class*='away']"
                                             ).last_child.css_first("a").text()
            team_home_score, team_away_score = _duel_info.css_first(
                "div[class*='score']").child.child.text().split('-')
            _match_status = _duel_info.css_first("div[class*='score']"
                                                 ).last_child.last_child.text()

            result = MatchData(league=league,
                               round_num=int(re.search(
                                   r'\d+', round_num).group()),
                               start_time=start_time,
                               team_home=team_home,
                               team_away=team_away,
                               score_team_home=team_home_score,
                               score_team_away=team_away_score
                               )
        else:
            result = None
        logger.info(f"{result} returned")
        return result
