"""Initial documentation of web scraping."""

from importlib.metadata import version as _version


try:
    __version__ = _version("cqscraper")
except Exception:
    # Local copy or not installed with setuptools.
    # Disable minimum version checks on downstream libraries.
    __version__ = "999"
