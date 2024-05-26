import json
import concurrent.futures
import validators
from pydantic import BaseModel, ValidationError
from typing import List, Dict
from cqscraper.lister import Lister, PageFetcher, PageParser, LinkExtractor
from cqscraper.crawler import (
    Crawler,
    ProductParser,
    ProductDataExtractor,
    ProductDataFormatter,
)
import cqscraper.confs


class Product(BaseModel):
    """
    Pydantic model for product data.

    Attributes:
        id (str): The product ID.
        name (str): The product name.
        CAS (str): The CAS number.
        structure (str): The chemical structure.
        smiles (str): The SMILES notation.
        description (str): The product description.
        molecular_weight (str): The molecular weight.
        url (str): The product URL.
        image_path (str): The path to the product image.
        img (str): The product image.
        pdf_msds (str): The PDF MSDS file.
        synonyms (List[str]): List of synonyms for the product.
        packaging (Dict[str, str]): Packaging information.
    """

    id: str
    name: str
    CAS: str
    structure: str
    smiles: str
    description: str
    molecular_weight: str
    url: str
    image_path: str
    img: str
    pdf_msds: str
    synonyms: List[str]
    packaging: Dict[str, str]


class ProductScraper:
    """
    A class to scrape product data from a website.

    Methods:
        fetch_product_urls(): Fetches the product URLs.
        crawl_product_data(product_urls): Crawls product data from the URLs.
        validate_products(raw_data): Validates the crawled product data.
        save_results(data): Saves the validated product data to a file.
        run(): Executes the scraping process.
    """

    def __init__(self, product_url: str, output_file: str, num_crawlers: int):
        """
        Initializes the ProductScraper with configuration parameters.

        Initializes de dependencies for the Lister

        Args:
            product_url (str): The URL to fetch product data from.
            output_file (str): The file to save the scraped product data.
            num_crawlers (int): The number of parallel crawlers to run.
        """
        self.product_url = product_url
        self.output_file = output_file
        self.num_crawlers = num_crawlers
        self.fetcher = PageFetcher()
        self.parser = PageParser()
        self.extractor = LinkExtractor()
        self.crawler_parser = ProductParser()
        self.crawler_extractor = ProductDataExtractor()
        self.crawler_formatter = ProductDataFormatter()

    def fetch_product_urls(self) -> List[str]:
        """
        Fetches the product URLs from the specified product URL.

        Returns:
            List[str]: A list of product URLs.
        """
        lister = Lister(self.product_url, self.fetcher, self.parser, self.extractor)
        try:
            return lister.get_product_urls()
        except Exception as e:
            print(f"Error fetching product URLs: {e}")
            return []

    def crawl_product_data(self, product_urls: List[str]) -> List[Dict]:
        """
        Crawls product data from the given product URLs using multiple crawlers.

        Args:
            product_urls (List[str]): A list of product URLs to crawl.

        Returns:
            List[Dict]: A list of dictionaries containing raw product data.
        """
        with concurrent.futures.ThreadPoolExecutor(
            max_workers=self.num_crawlers
        ) as executor:
            crawlers = [
                Crawler(
                    url,
                    self.crawler_parser,
                    self.crawler_extractor,
                    self.crawler_formatter,
                )
                for url in product_urls
            ]
            return list(executor.map(lambda crawler: crawler.crawl(), crawlers))

    def validate_products(self, raw_data: List[Dict]) -> List[Dict]:
        """
        Validates the crawled product data using the Product Pydantic model.

        Args:
            raw_data (List[Dict]): A list of dictionaries containing raw product data.

        Returns:
            List[Dict]: A list of validated product data dictionaries.
        """
        validated_results = []
        for result in raw_data:
            try:
                validated_product = Product(**result)
                validated_results.append(validated_product.dict())
            except ValidationError as e:
                print(f"Validation error for product data: {e}")
        return validated_results

    def save_results(self, data: List[Dict]):
        """
        Saves the validated product data to a JSON file.

        Args:
            data (List[Dict]): A list of validated product data dictionaries.
        """
        output_data = json.dumps(data, indent=4)
        try:
            with open(self.output_file, "w") as f:
                f.write(output_data)
        except IOError as e:
            print(f"Error writing results to file: {e}")

    def run(self):
        """
        Executes the scraping process: fetches URLs, crawls data, validates it, and saves the results.
        """
        product_urls = self.fetch_product_urls()
        validated_products_urls = []
        for url in product_urls:
            if validators.url(url):
                validated_products_urls.append(url)

        if not validated_products_urls:
            print("No product URLs found. Exiting.")
            return

        raw_data = self.crawl_product_data(validated_products_urls)
        validated_data = self.validate_products(raw_data)
        self.save_results(validated_data)
