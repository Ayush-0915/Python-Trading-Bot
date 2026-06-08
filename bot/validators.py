"""
Input validation layer for the Binance Futures Trading Bot.
This module validates and normalizes all input parameters before sending them to the Binance API client.
"""

import re
from typing import Any, Optional, Union

# Custom Exceptions
class ValidationError(ValueError):
    """Base validation exception class."""
    pass

class InvalidSymbolError(ValidationError):
    """Exception raised when the trading symbol format is invalid."""
    pass

class InvalidSideError(ValidationError):
    """Exception raised when the order side is invalid."""
    pass

class InvalidOrderTypeError(ValidationError):
    """Exception raised when the order type is invalid."""
    pass

class InvalidQuantityError(ValidationError):
    """Exception raised when the quantity is invalid."""
    pass

class InvalidPriceError(ValidationError):
    """Exception raised when the price is invalid."""
    pass


def validate_symbol(symbol: Any) -> str:
    """
    Validates and normalizes the trading symbol.
    
    Args:
        symbol: The symbol to validate (e.g., 'btcusdt', 'ETHUSDT').
        
    Returns:
        str: The normalized uppercase symbol.
        
    Raises:
        InvalidSymbolError: If the symbol is not a string, is empty, or is formatted incorrectly.
    """
    if not isinstance(symbol, str):
        raise InvalidSymbolError(
            f"Symbol must be a string, got {type(symbol).__name__}."
        )
    
    cleaned_symbol = symbol.strip().upper()
    
    if not cleaned_symbol:
        raise InvalidSymbolError("Symbol cannot be empty.")
    
    # Binance symbols are alphanumeric, uppercase, usually 5-15 characters long
    # We validate that it consists of only uppercase letters and digits, and is between 3 and 20 characters.
    if not re.match(r"^[A-Z0-9]{3,20}$", cleaned_symbol):
        raise InvalidSymbolError(
            f"Symbol '{cleaned_symbol}' has an invalid format. Must be alphanumeric and 3-20 characters long."
        )
        
    return cleaned_symbol


def validate_side(side: Any) -> str:
    """
    Validates and normalizes the order side.
    
    Args:
        side: The order side ('BUY' or 'SELL', case-insensitive).
        
    Returns:
        str: The normalized uppercase side ('BUY' or 'SELL').
        
    Raises:
        InvalidSideError: If the side is not a string or is not 'BUY' or 'SELL'.
    """
    if not isinstance(side, str):
        raise InvalidSideError(
            f"Order side must be a string, got {type(side).__name__}."
        )
        
    cleaned_side = side.strip().upper()
    
    if cleaned_side not in ("BUY", "SELL"):
        raise InvalidSideError(
            f"Invalid order side '{cleaned_side}'. Supported values are 'BUY' or 'SELL'."
        )
        
    return cleaned_side


def validate_order_type(order_type: Any) -> str:
    """
    Validates and normalizes the order type.
    
    Args:
        order_type: The type of order ('MARKET' or 'LIMIT', case-insensitive).
        
    Returns:
        str: The normalized uppercase order type ('MARKET' or 'LIMIT').
        
    Raises:
        InvalidOrderTypeError: If the order type is not a string or is not 'MARKET' or 'LIMIT'.
    """
    if not isinstance(order_type, str):
        raise InvalidOrderTypeError(
            f"Order type must be a string, got {type(order_type).__name__}."
        )
        
    cleaned_type = order_type.strip().upper()
    
    if cleaned_type not in ("MARKET", "LIMIT"):
        raise InvalidOrderTypeError(
            f"Invalid order type '{cleaned_type}'. Supported values are 'MARKET' or 'LIMIT'."
        )
        
    return cleaned_type


def validate_quantity(quantity: Any) -> float:
    """
    Validates and normalizes the order quantity.
    
    Args:
        quantity: The quantity to validate (numeric or numeric string).
        
    Returns:
        float: The normalized float quantity.
        
    Raises:
        InvalidQuantityError: If quantity is not numeric, cannot be parsed, or is <= 0.
    """
    if quantity is None:
        raise InvalidQuantityError("Quantity is required and cannot be None.")
        
    try:
        float_quantity = float(quantity)
    except (ValueError, TypeError):
        raise InvalidQuantityError(
            f"Quantity must be numeric or a numeric string, got '{quantity}'."
        )
        
    if float_quantity <= 0.0:
        raise InvalidQuantityError(
            f"Quantity must be greater than 0, got {float_quantity}."
        )
        
    return float_quantity


def validate_price(price: Any, order_type: str) -> Optional[float]:
    """
    Validates and normalizes the price. Price is required for LIMIT orders.
    
    Args:
        price: The price to validate (numeric or numeric string).
        order_type: The normalized order type (e.g., 'LIMIT', 'MARKET').
        
    Returns:
        float or None: The normalized float price, or None if the order type is MARKET and no price is provided.
        
    Raises:
        InvalidPriceError: If the price is missing or invalid for LIMIT orders, or is <= 0.
    """
    # For MARKET orders, price is not needed/used
    if order_type == "MARKET":
        if price is None or price == "":
            return None
            
    # For LIMIT orders, price is strictly required
    if price is None or price == "":
        raise InvalidPriceError(
            f"Price is required for '{order_type}' orders."
        )
        
    try:
        float_price = float(price)
    except (ValueError, TypeError):
        raise InvalidPriceError(
            f"Price must be numeric or a numeric string, got '{price}'."
        )
        
    if float_price <= 0.0:
        raise InvalidPriceError(
            f"Price must be greater than 0, got {float_price}."
        )
        
    return float_price
