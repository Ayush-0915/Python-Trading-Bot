"""
Binance Futures Testnet Client wrapper.
This module handles communication with the Binance Futures Testnet API.
"""

import os
from typing import Any, Dict, Union
import requests
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException
from dotenv import load_dotenv
from bot.logging_config import setup_logger

# Load environment variables from .env file
load_dotenv()

# Initialize logger for the client module
logger = setup_logger("client")

# Custom Exceptions
class BinanceClientError(Exception):
    """Base exception class for all BinanceClient errors."""
    pass

class MissingCredentialsError(BinanceClientError):
    """Exception raised when API credentials are missing from the environment or input."""
    pass

class InvalidCredentialsError(BinanceClientError):
    """Exception raised when API credentials are invalid or rejected by Binance."""
    pass

class BinanceAPIError(BinanceClientError):
    """Exception raised when Binance API returns an error response."""
    def __init__(self, message: str, code: int, status_code: int):
        super().__init__(message)
        self.code = code
        self.status_code = status_code

class BinanceNetworkError(BinanceClientError):
    """Exception raised when connection or network request failures occur."""
    pass

class BinanceTimeoutError(BinanceClientError):
    """Exception raised when a request to Binance times out."""
    pass

class UnexpectedClientError(BinanceClientError):
    """Exception raised for any other unexpected failures."""
    pass


class BinanceClient:
    """
    Client wrapper for Binance Futures Testnet API.
    Responsible ONLY for low-level API communication.
    """
    
    def __init__(self, api_key: str | None = None, api_secret: str | None = None) -> None:
        """
        Initializes the Binance Client.
        
        Args:
            api_key: Binance API Key. If not provided, loads from BINANCE_API_KEY env var.
            api_secret: Binance API Secret. If not provided, loads from BINANCE_API_SECRET env var.
            
        Raises:
            MissingCredentialsError: If API credentials are not found.
            UnexpectedClientError: If client initialization fails.
        """
        # Prioritize passed args, fall back to environment variables
        self.api_key = api_key or os.getenv("BINANCE_API_KEY")
        self.api_secret = api_secret or os.getenv("BINANCE_API_SECRET")
        
        if not self.api_key or not self.api_secret:
            err_msg = "Missing API credentials. Please set BINANCE_API_KEY and BINANCE_API_SECRET in environment."
            logger.error(err_msg)
            raise MissingCredentialsError(err_msg)
            
        try:
            logger.info("Initializing Binance client for Futures Testnet")
            self._client = Client(
                api_key=self.api_key,
                api_secret=self.api_secret,
                testnet=True
            )
            logger.info("Binance client initialized successfully")
        except Exception as e:
            err_msg = f"Failed to initialize python-binance Client: {e}"
            logger.error(err_msg)
            raise UnexpectedClientError(err_msg) from e

    def _handle_exception(self, e: Exception) -> Exception:
        """
        Translates python-binance/requests exceptions to custom BinanceClient exceptions and logs them.
        """
        if isinstance(e, BinanceAPIException):
            # API credential related error codes:
            # -1022: Signature for this request is not valid
            # -2008: Invalid Api-Key ID
            # -2015: Invalid API-key, IP, or permissions
            if e.code in (-1022, -2008, -2015):
                wrapped_err = InvalidCredentialsError(
                    f"Authentication failed: {e.message} (Binance Error Code: {e.code})"
                )
                logger.error(f"Authentication failure: {wrapped_err}")
                return wrapped_err
                
            wrapped_err = BinanceAPIError(
                message=f"Binance API Error: {e.message}",
                code=e.code,
                status_code=e.status_code
            )
            logger.error(f"API request failed: {wrapped_err}")
            return wrapped_err
            
        elif isinstance(e, BinanceRequestException):
            wrapped_err = BinanceNetworkError(f"Network connection failed: {e}")
            logger.error(f"Network failure: {wrapped_err}")
            return wrapped_err
            
        elif isinstance(e, requests.exceptions.Timeout):
            wrapped_err = BinanceTimeoutError(f"Request timed out: {e}")
            logger.error(f"Timeout failure: {wrapped_err}")
            return wrapped_err
            
        elif isinstance(e, requests.exceptions.RequestException):
            wrapped_err = BinanceNetworkError(f"HTTP network exception occurred: {e}")
            logger.error(f"HTTP connection failure: {wrapped_err}")
            return wrapped_err
            
        wrapped_err = UnexpectedClientError(f"An unexpected client error occurred: {e}")
        logger.error(f"Unexpected error: {wrapped_err}")
        return wrapped_err

    def ping(self) -> Dict[str, Any]:
        """
        Pings the Binance Futures Testnet server to test connectivity.
        
        Returns:
            Dict: Full response from Binance (normally empty dictionary {}).
            
        Raises:
            BinanceNetworkError: If connection/network fails.
            BinanceTimeoutError: If request times out.
            BinanceAPIError: If API returns an error response.
            UnexpectedClientError: For other unexpected failures.
        """
        logger.info("Sending ping request to Binance Futures Testnet")
        try:
            response = self._client.futures_ping()
            logger.info("Ping successful")
            return response
        except Exception as e:
            raise self._handle_exception(e) from e

    def get_server_time(self) -> Dict[str, Any]:
        """
        Retrieves the current Binance server time.
        
        Returns:
            Dict: Full response from Binance containing server time.
            
        Raises:
            BinanceNetworkError: If connection/network fails.
            BinanceTimeoutError: If request times out.
            BinanceAPIError: If API returns an error response.
            UnexpectedClientError: For other unexpected failures.
        """
        logger.info("Retrieving server time from Binance Futures Testnet")
        try:
            response = self._client.futures_time()
            logger.info(f"Server time retrieved: {response.get('serverTime')}")
            return response
        except Exception as e:
            raise self._handle_exception(e) from e

    def create_market_order(
        self, symbol: str, side: str, quantity: Union[float, str]
    ) -> Dict[str, Any]:
        """
        Places a market order on Binance Futures Testnet.
        
        Args:
            symbol: Trading pair symbol (e.g., 'BTCUSDT').
            side: Order side ('BUY' or 'SELL').
            quantity: Order quantity.
            
        Returns:
            Dict: Full Binance API response.
            
        Raises:
            InvalidCredentialsError: If credentials are invalid.
            BinanceNetworkError: If connection/network fails.
            BinanceTimeoutError: If request times out.
            BinanceAPIError: If API returns an error response.
            UnexpectedClientError: For other unexpected failures.
        """
        logger.info(f"Placing MARKET order: {side} {quantity} {symbol}")
        try:
            response = self._client.futures_create_order(
                symbol=symbol,
                side=side,
                type="MARKET",
                quantity=quantity,
                recvWindow=60000
            )
            logger.info(f"MARKET order placed successfully. Order ID: {response.get('orderId')}")
            return response
        except Exception as e:
            raise self._handle_exception(e) from e

    def create_limit_order(
        self, symbol: str, side: str, quantity: Union[float, str], price: Union[float, str]
    ) -> Dict[str, Any]:
        """
        Places a limit order on Binance Futures Testnet.
        
        Args:
            symbol: Trading pair symbol (e.g., 'BTCUSDT').
            side: Order side ('BUY' or 'SELL').
            quantity: Order quantity.
            price: Order price.
            
        Returns:
            Dict: Full Binance API response.
            
        Raises:
            InvalidCredentialsError: If credentials are invalid.
            BinanceNetworkError: If connection/network fails.
            BinanceTimeoutError: If request times out.
            BinanceAPIError: If API returns an error response.
            UnexpectedClientError: For other unexpected failures.
        """
        logger.info(f"Placing LIMIT order: {side} {quantity} {symbol} @ {price}")
        try:
            response = self._client.futures_create_order(
                symbol=symbol,
                side=side,
                type="LIMIT",
                quantity=quantity,
                price=price,
                timeInForce="GTC",  # Default Good Till Cancelled
                recvWindow=60000
            )
            logger.info(f"LIMIT order placed successfully. Order ID: {response.get('orderId')}")
            return response
        except Exception as e:
            raise self._handle_exception(e) from e

