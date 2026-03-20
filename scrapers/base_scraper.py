from abc import ABC, abstractmethod
import logging
import requests

class BaseScraper(ABC):
    """Abstract Base Scraper Class."""

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    def start_scraping(self):
        """Method to start scraping. Must be implemented by subclasses."""
        pass

    @abstractmethod
    def parse_data(self, response):
        """Method to parse data from the response. Must be implemented by subclasses."""
        pass

    def make_request(self, url):
        """Method to make an HTTP request and return the response."""
        try:
            self.logger.info(f'Making request to {url}')
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for bad responses
            return response
        except requests.RequestException as e:
            self.logger.error(f'Request failed: {e}')
            return None

    def log_info(self, message):
        """Utility method to log an info message."""
        self.logger.info(message)

    def log_error(self, message):
        """Utility method to log an error message."""
        self.logger.error(message)