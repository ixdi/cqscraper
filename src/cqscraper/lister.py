from abc import ABC, abstractmethod
from typing import List
from bs4 import BeautifulSoup
import requests
import cqscraper.confs as confs

""" Interfaces for the lister module. """


class IPageFetcher(ABC):
    @abstractmethod
    def fetch_page(self, url: str) -> str:
        pass


class IPageParser(ABC):
    @abstractmethod
    def parse_page(self, page_content: str) -> BeautifulSoup:
        pass


class ILinkExtractor(ABC):
    @abstractmethod
    def extract_links(self, parsed_page: BeautifulSoup) -> List[str]:
        pass


""" Implementations of the interfaces. """


class PageFetcher(IPageFetcher):
    def fetch_page(self, url: str) -> str:
        response = requests.get(url)
        response.raise_for_status()  # Ensure we catch any HTTP errors
        return response.text


class PageParser(IPageParser):
    def parse_page(self, page_content: str) -> BeautifulSoup:
        return BeautifulSoup(page_content, "lxml")


class LinkExtractor(ILinkExtractor):
    def extract_links(self, parsed_page: BeautifulSoup) -> List[str]:
        links = parsed_page.find_all("a", attrs={"class", confs.PRODUCT_LINK_CLASS})
        return [link["href"] for link in links]


""" Lister module that fetches product URLs from a given URL. """


class Lister:
    """Class to list product URLs from a webpage."""

    def __init__(
        self,
        base_url: str,
        fetcher: IPageFetcher,
        parser: IPageParser,
        extractor: ILinkExtractor,
    ):
        """
        Initializes the Lister class.

        Args:
            base_url (str): The base URL to fetch product URLs from.
            fetcher (IPageFetcher): The fetcher instance to fetch pages.
            parser (IPageParser): The parser instance to parse pages.
            extractor (ILinkExtractor): The extractor instance to extract links.
        """
        self.base_url = base_url
        self.fetcher = fetcher
        self.parser = parser
        self.extractor = extractor

    def get_product_urls(self) -> List[str]:
        """
        Fetches product URLs from the provided base URL.

        Check that page exists before getting the content.

        Returns:
            List[str]: The list of product URLs.
        """
        product_urls = []
        page = 1
        while True:
            url = f"{self.base_url}{confs.PRODUCT_URL_NEXT}{page}"
            response = requests.get(url)
            if response.status_code == 200:
                page_content = self.fetcher.fetch_page(url)
                print(f"Fetching page {page} from {url}")
                parsed_page = self.parser.parse_page(page_content)
                links_hrefs_list = self.extractor.extract_links(parsed_page)
                print(f"LINKS :: {len(links_hrefs_list)}")

                if not links_hrefs_list:
                    break

                product_urls.extend(links_hrefs_list)
                page += 1
            else:
                break

        return product_urls
