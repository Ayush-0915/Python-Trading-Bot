import unittest
from unittest.mock import MagicMock, patch
import requests
from binance.exceptions import BinanceAPIException, BinanceRequestException
from bot.client import (
    BinanceClient,
    MissingCredentialsError,
    InvalidCredentialsError,
    BinanceAPIError,
    BinanceNetworkError,
    BinanceTimeoutError,
    UnexpectedClientError
)

class TestBinanceClientExceptions(unittest.TestCase):
    def setUp(self):
        # Initialize the client with dummy credentials to bypass the missing check
        self.client = BinanceClient(api_key="test_key", api_secret="test_secret")

    def test_handle_exception_invalid_credentials(self):
        # Test error code -2008 (Invalid API Key)
        mock_response = MagicMock()
        api_exception = BinanceAPIException(
            response=mock_response,
            status_code=401,
            text='{"code": -2008, "msg": "Invalid Api-Key ID."}'
        )
        wrapped = self.client._handle_exception(api_exception)
        self.assertIsInstance(wrapped, InvalidCredentialsError)
        self.assertIn("Authentication failed", str(wrapped))

    def test_handle_exception_api_error(self):
        # Test generic Binance API error code -1001
        mock_response = MagicMock()
        api_exception = BinanceAPIException(
            response=mock_response,
            status_code=400,
            text='{"code": -1001, "msg": "Internal error."}'
        )
        wrapped = self.client._handle_exception(api_exception)
        self.assertIsInstance(wrapped, BinanceAPIError)
        self.assertEqual(wrapped.code, -1001)
        self.assertEqual(wrapped.status_code, 400)

    def test_handle_exception_network_request_error(self):
        # Test BinanceRequestException
        req_exception = BinanceRequestException("Connection lost")
        wrapped = self.client._handle_exception(req_exception)
        self.assertIsInstance(wrapped, BinanceNetworkError)

    def test_handle_exception_timeout_error(self):
        # Test requests.exceptions.Timeout
        timeout_exception = requests.exceptions.Timeout("Request timed out")
        wrapped = self.client._handle_exception(timeout_exception)
        self.assertIsInstance(wrapped, BinanceTimeoutError)

    def test_handle_exception_http_network_error(self):
        # Test requests.exceptions.RequestException
        req_exception = requests.exceptions.RequestException("HTTP error")
        wrapped = self.client._handle_exception(req_exception)
        self.assertIsInstance(wrapped, BinanceNetworkError)

    def test_handle_exception_unexpected_error(self):
        # Test generic python exception
        generic_exception = ValueError("Unexpected value")
        wrapped = self.client._handle_exception(generic_exception)
        self.assertIsInstance(wrapped, UnexpectedClientError)

if __name__ == "__main__":
    unittest.main()
