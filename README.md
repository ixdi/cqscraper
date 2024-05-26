# Web Scraper for Product Data

This project contains a web scraper to list product URLs from a given page, and then crawl each product page to extract specific information.
Stores the results as a JSON file.

## Setup

- Install the required packages:

```sh
pip install -r requirements.txt
```

It would be much better to use a virtual environment and then install the package itself.

To install the package itself with its dependencies in editable mode:

```sh
pip install -e .
```

- Run the scraper:

```sh
python src/cqscraper -c <number_of_crawlers>
```

## Description

- `Lister`: Fetches product URLs from a provided base URL.
- `Crawler`: Extracts data from each product page.
- `Scraper`: Orchestrates the lister and crawler.
- `Helpers`: Contains utility functions for image processing and PDF extraction.
- `Confs`: Contains definitions like products urls, output file name, etc.

## Testing

```sh
pytest tests
```

## Strategy

- Use a ProductScraper class to orchestrate the lister and crawler.
- The Lister uses the `requests` library to fetch the HTML content of the page, and `lxml` to parse the HTML content.
- The Crawler uses `BeautifulSoup` to parse the HTML content.
  - Get the main div containing the product information.
  - Pass the content to string
  - Extract the information searching for specific strings
  - Some data also uses BeautifulSoup methods to extract the information

## Uniformed Tests with tox

Thanks to [Tox](https://tox.readthedocs.io/en/latest/), we can have a unified testing platform that runs all tests in controlled environments and is reproducible for all developers. In other words, it is a way to welcome (*force*) all developers to follow the same rules.

The `tox` testing setup is defined in a configuration file, the [`tox.ini`](https://github.com/joaomcteixeira/python-project-skeleton/blob/latest/tox.ini), which contains all the operations that are performed during the test phase. Therefore, to run the unified test suite, developers just need to execute `tox`, provided [tox is installed](https://tox.readthedocs.io/en/latest/install.html) in the Python environment in use.

```sh
pip install tox
```

One of the greatest advantages of using `tox` together with the src layout is that unit tests actually perform on the installed source (our package) inside an isolated deployment environment. In other words, tests are performed in an environment simulating a post-installation state instead of a pre-deploy/development environment. Under this setup, there is no need, in general cases, to distribute unit test scripts along with the actual source, in my honest opinion - see [`MANIFEST.in`](https://github.com/joaomcteixeira/python-project-skeleton/blob/main/MANIFEST.in).

Before creating a Pull Request from your branch, certify that all the tests pass correctly by running:

```sh
tox
```

These are exactly the same tests that will be performed online in the GitHub Actions.

Also, you can run individual environments if you wish to test only specific functionalities, for example:

```sh
tox -e lint  # code style
tox -e radon # code quality
tox -e safety  # check for security vulnerabilities
tox -e test  # runs unit tests
```

## Improvements

- Add more tests, for all the modules
- Add better error handling with a logging
- Use a database to store the results
- Use ReadTheDocs to document the project or something similar
- Improve tox for testing against different Python versions, better environments, etc
- Add testing coverage
- Integrate with more githuib actions and hooks
