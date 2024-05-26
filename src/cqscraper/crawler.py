import requests
from bs4 import BeautifulSoup
from abc import ABC, abstractmethod
from typing import List, Dict
from cqscraper.helpers import process_image, extract_pdf_info


class IParser(ABC):
    """Interface for parsing web content."""

    @abstractmethod
    def parse_content(self, url: str) -> BeautifulSoup:
        pass


class ProductParser(IParser):
    """Concrete implementation of IParser for product pages."""

    def parse_content(self, url: str) -> BeautifulSoup:
        response = requests.get(url)
        return BeautifulSoup(response.content, "html.parser")


class IDataExtractor(ABC):
    """Interface for extracting data from parsed content."""

    @abstractmethod
    def extract_data(self, product_url: str, parsed_content: BeautifulSoup) -> dict:
        pass


class ProductDataExtractor(IDataExtractor):
    """Concrete implementation of IDataExtractor for product data."""

    def search_text(self, strings: List[str], searched_text: str) -> str:
        found = False
        for string in strings:
            if found == True:
                return string.strip()
            if string == searched_text:
                found = True
        return ""

    def search_text_between(
        self, strings: List[str], start_text: str, end_text: str, join_char: str
    ) -> str:
        found = False
        joining = False
        text_joined = ""
        for string in strings:
            if found == True:
                return string.strip()
            if joining == True:
                text_joined = text_joined + join_char + string
            if string == start_text:
                joining = True
                text_joined = string
            if string == end_text:
                found = True
        return ""

    def extract_data(self, product_url: str, parsed_content: BeautifulSoup) -> dict:
        print(f"Extracting data from {product_url}")
        strings = parsed_content.find(
            name="div", attrs={"class": "product"}
        ).stripped_strings
        return {
            "product_id": self.search_text(strings, "Product number:"),
            "product_name": parsed_content.find(
                "h1", attrs={"class": "product-title"}, recursive=True
            ).text.strip(),
            "cas": self.search_text(strings, "CAS number:"),
            "structure": self.search_text_between(
                strings, "Molecular formula:", "Molecular weight:", ""
            ),
            "smiles": self.search_text(strings, "Smiles:"),
            "description": "None",
            "molecular_weight": self.search_text(strings, "Molecular weight:"),
            "url": product_url,
            "image_url": (
                parsed_content.find(name="div", attrs={"class": "product"}).find_next(
                    "img"
                )["src"]
                if parsed_content.find(
                    name="div", attrs={"class": "product"}
                ).find_next("img")
                else "None"
            ),
            "pdf_url": (
                parsed_content.find(name="a", text="Download")["href"]
                if parsed_content.find(name="a", text="Download")
                else "None"
            ),
            "synonyms": self.search_text_between(
                strings, "Synonyms:", "Molecular formula:", ","
            ).split(","),
            "packaging": {},
        }


class IFormatter(ABC):
    """Interface for formatting extracted data."""

    @abstractmethod
    def format(self, extracted_data: dict, image_path: str, pdf_info: dict) -> dict:
        pass


class ProductDataFormatter(IFormatter):
    """Concrete implementation of IFormatter for product data."""

    def format(self, extracted_data: dict, image_path: str, pdf_info: dict) -> dict:
        return {
            "id": extracted_data["product_id"],
            "name": extracted_data["product_name"],
            "CAS": extracted_data["cas"],
            "structure": extracted_data["structure"],
            "smiles": extracted_data["smiles"],
            "description": extracted_data["description"],
            "molecular_weight": extracted_data["molecular_weight"],
            "url": extracted_data["url"],
            "image_path": image_path,
            "img": image_path,
            "pdf_msds": pdf_info,
            "synonyms": extracted_data["synonyms"],
            "packaging": extracted_data["packaging"],
        }


class Crawler:
    """Class to crawl individual product pages and extract data."""

    def __init__(
        self,
        product_url: str,
        parser: IParser,
        extractor: IDataExtractor,
        formatter: IFormatter,
    ):
        """Initializes the Crawler class.

        Args:
            product_url (str): The URL of the product page to crawl
            parser (IParser): The parser to use for parsing the content
            extractor (IDataExtractor): The data extractor to use
            formatter (IFormatter): The formatter to use for formatting the data
        """
        self.product_url = product_url
        self.parser = parser
        self.extractor = extractor
        self.formatter = formatter

    def crawl(self) -> dict:
        """Fetches and processes data from a product page.

        Returns:
            dict: The product data in json format.
        """
        parsed_content = self.parser.parse_content(self.product_url)
        extracted_data = self.extractor.extract_data(self.product_url, parsed_content)
        image_path = process_image(extracted_data["image_url"])
        pdf_info = extract_pdf_info(extracted_data["pdf_url"])
        json_data = self.formatter.format(extracted_data, image_path, pdf_info)
        return json_data
