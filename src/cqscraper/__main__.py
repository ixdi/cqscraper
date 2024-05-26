import argparse
from cqscraper.product_scraper import ProductScraper
import cqscraper.confs as configs


def main():
    """
    Parses command-line arguments and runs the product scraper.
    """
    parser = argparse.ArgumentParser(description="Web scraper for product data.")
    parser.add_argument(
        "-c",
        "--crawlers",
        type=int,
        default=1,
        help="Number of parallel crawlers to run.",
    )
    args = parser.parse_args()

    scraper = ProductScraper(
        product_url=configs.PRODUCTS_URL,
        output_file=configs.FILE_NAME_PRODUCTS_RESULTS,
        num_crawlers=args.crawlers,
    )
    scraper.run()


if __name__ == "__main__":
    main()
