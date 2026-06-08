"""
Order Processing Layer for the Binance Futures Trading Bot.
Coordinates parameter validation, logging, and sending orders to the Binance API.
"""

from typing import Any, Dict, Optional
from bot.client import BinanceClient, BinanceClientError
from bot.validators import (
    validate_symbol,
    validate_side,
    validate_quantity,
    validate_price,
    ValidationError
)
from bot.logging_config import setup_logger

# Initialize logger
logger = setup_logger("orders")

class OrderManager:
    """
    Coordinates validation, logging, and execution of trading orders on Binance Futures.
    """
    
    def __init__(self, client: Optional[BinanceClient] = None) -> None:
        """
        Initializes the OrderManager.
        
        Args:
            client: Optional BinanceClient instance. If not provided, a new instance is created.
        """
        try:
            self.client = client or BinanceClient()
        except Exception as e:
            logger.error(f"Failed to initialize BinanceClient: {e}")
            raise e

    def place_market_order(
        self, symbol: str, side: str, quantity: float
    ) -> Dict[str, Any]:
        """
        Places a market order after validating inputs and logging.
        
        Args:
            symbol: Trading pair (e.g. 'BTCUSDT').
            side: Order side ('BUY' or 'SELL').
            quantity: Order quantity.
            
        Returns:
            Dict: Structured success or failure response.
        """
        order_type = "MARKET"
        try:
            # Step 1: Validate inputs
            valid_symbol = validate_symbol(symbol)
            valid_side = validate_side(side)
            valid_qty = validate_quantity(quantity)
            
            # Step 2: Log order request
            logger.info(
                f"Processing {order_type} order request | Symbol: {valid_symbol} | Side: {valid_side} | Quantity: {valid_qty}"
            )
            
            # Step 3: Submit order through BinanceClient
            response = self.client.create_market_order(
                symbol=valid_symbol,
                side=valid_side,
                quantity=valid_qty
            )
            
            # Step 4: Log Binance response
            order_id = response.get("orderId")
            status = response.get("status")
            executed_qty = response.get("executedQty")
            avg_price = response.get("avgPrice")
            
            logger.info(
                f"Binance response received for {order_type} order | Order ID: {order_id} | Status: {status} | "
                f"Executed Qty: {executed_qty} | Avg Price: {avg_price} | Full Response: {response}"
            )
            
            # Step 5: Return structured response
            return {
                "success": True,
                "order_id": str(order_id) if order_id is not None else "",
                "status": str(status) if status is not None else "",
                "executed_qty": str(executed_qty) if executed_qty is not None else "0.0",
                "avg_price": str(avg_price) if avg_price is not None else "0.0"
            }
            
        except ValidationError as e:
            err_msg = f"Validation failed for {order_type} order: {e}"
            logger.error(err_msg)
            return {"success": False, "error": err_msg}
            
        except BinanceClientError as e:
            err_msg = f"Binance API/Network error occurred during {order_type} order: {e}"
            logger.error(err_msg)
            return {"success": False, "error": err_msg}
            
        except Exception as e:
            err_msg = f"Unexpected system error occurred during {order_type} order: {e}"
            logger.error(err_msg)
            return {"success": False, "error": err_msg}

    def place_limit_order(
        self, symbol: str, side: str, quantity: float, price: float
    ) -> Dict[str, Any]:
        """
        Places a limit order after validating inputs and logging.
        
        Args:
            symbol: Trading pair (e.g. 'BTCUSDT').
            side: Order side ('BUY' or 'SELL').
            quantity: Order quantity.
            price: Order limit price.
            
        Returns:
            Dict: Structured success or failure response.
        """
        order_type = "LIMIT"
        try:
            # Step 1: Validate all inputs
            valid_symbol = validate_symbol(symbol)
            valid_side = validate_side(side)
            valid_qty = validate_quantity(quantity)
            valid_price = validate_price(price, order_type)
            
            # Step 2: Log order request
            logger.info(
                f"Processing {order_type} order request | Symbol: {valid_symbol} | Side: {valid_side} | "
                f"Quantity: {valid_qty} | Price: {valid_price}"
            )
            
            # Step 3: Submit order through BinanceClient
            response = self.client.create_limit_order(
                symbol=valid_symbol,
                side=valid_side,
                quantity=valid_qty,
                price=valid_price
            )
            
            # Step 4: Log Binance response
            order_id = response.get("orderId")
            status = response.get("status")
            executed_qty = response.get("executedQty")
            avg_price = response.get("avgPrice")
            
            logger.info(
                f"Binance response received for {order_type} order | Order ID: {order_id} | Status: {status} | "
                f"Executed Qty: {executed_qty} | Avg Price: {avg_price} | Full Response: {response}"
            )
            
            # Step 5: Return structured response
            return {
                "success": True,
                "order_id": str(order_id) if order_id is not None else "",
                "status": str(status) if status is not None else "",
                "executed_qty": str(executed_qty) if executed_qty is not None else "0.0",
                "avg_price": str(avg_price) if avg_price is not None else "0.0"
            }
            
        except ValidationError as e:
            err_msg = f"Validation failed for {order_type} order (Price: {price}): {e}"
            logger.error(err_msg)
            return {"success": False, "error": err_msg}
            
        except BinanceClientError as e:
            err_msg = f"Binance API/Network error occurred during {order_type} order: {e}"
            logger.error(err_msg)
            return {"success": False, "error": err_msg}
            
        except Exception as e:
            err_msg = f"Unexpected system error occurred during {order_type} order: {e}"
            logger.error(err_msg)
            return {"success": False, "error": err_msg}
