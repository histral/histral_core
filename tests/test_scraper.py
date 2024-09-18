import unittest
import requests

from unittest.mock import patch, MagicMock
from bs4 import BeautifulSoup
from histral_core.scraper import fetch_soup


class TestScraper(unittest.TestCase):
    """
    Unit tests for `histral_core.scraper` module
    """

    @patch("histral_core.scraper.requests.get")
    def test_fetch_soup_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.content = b"<html><body><h1>Test</h1></body></html>"
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        url = "http://example.com"
        soup = fetch_soup(url)
        self.assertIsInstance(soup, BeautifulSoup)
        self.assertEqual(soup.h1.text, "Test")

    @patch("histral_core.scraper.requests.get")
    def test_fetch_soup_http_error(self, mock_get):
        mock_get.side_effect = requests.exceptions.HTTPError("404 Not Found")

        url = "http://example.com"
        with patch("histral_core.scraper.Logger.error") as mock_log:
            soup = fetch_soup(url)
            self.assertIsNone(soup)
            self.assertTrue(mock_log.called)
            log_message = mock_log.call_args[0][0]
            self.assertIn("Failed to fetch URL", log_message)

    @patch("histral_core.scraper.requests.get")
    def test_fetch_soup_request_exception(self, mock_get):
        mock_get.side_effect = requests.exceptions.RequestException("Request failed")

        url = "http://example.com"
        with patch("histral_core.scraper.Logger.error") as mock_log:
            soup = fetch_soup(url)
            self.assertIsNone(soup)
            self.assertTrue(mock_log.called)
            log_message = mock_log.call_args[0][0]
            self.assertIn("Failed to fetch URL", log_message)


if __name__ == "__main__":
    unittest.main()
