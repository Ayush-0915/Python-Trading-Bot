import unittest
from unittest.mock import MagicMock
from bot.orders import OrderManager
from bot.client import BinanceClientError, MissingCredentialsError
from bot.validators import ValidationError

class TestOrderManager(unittest.TestCase):
    def setUp(self):
        self.mock_client = MagicMock()
        self.manager = OrderManager(client=self.mock_client)

    def test_place_market_order_success(self):
        # Setup mock client response
        self.mock_client.create_market_order.return_value = {
            "orderId": 123456789,
            "status": "FILLED",
            "executedQty": "0.100",
            "avgPrice": "65000.50"
        }
        
        result = self.manager.place_market_order("BTCUSDT", "BUY", 0.1)
        
        # Verify client was called with correct parameters
        self.mock_client.create_market_order.assert_called_once_with(
            symbol="BTCUSDT",
            side="BUY",
            quantity=0.1
        )
        
        # Verify structured response format
        self.assertTrue(result["success"])
        self.assertEqual(result["order_id"], "123456789")
        self.assertEqual(result["status"], "FILLED")
        self.assertEqual(result["executed_qty"], "0.100")
        self.assertEqual(result["avg_price"], "65000.50")

    def test_place_market_order_validation_error(self):
        # Pass an invalid side (must be BUY or SELL)
        result = self.manager.place_market_order("BTCUSDT", "HOLD", 0.1)
        
        # Client should not be called
        self.mock_client.create_market_order.assert_not_called()
        
        # Verify failure response format
        self.assertFalse(result["success"])
        self.assertIn("Validation failed", result["error"])

    def test_place_market_order_client_error(self):
        # Setup client to raise BinanceClientError
        self.mock_client.create_market_order.side_effect = BinanceClientError("API connection lost")
        
        result = self.manager.place_market_order("BTCUSDT", "BUY", 0.1)
        
        self.assertFalse(result["success"])
        self.assertIn("Binance API/Network error occurred", result["error"])

    def test_place_limit_order_success(self):
        # Setup mock client response
        self.mock_client.create_limit_order.return_value = {
            "orderId": 987654321,
            "status": "NEW",
            "executedQty": "0.000",
            "avgPrice": "0.0"
        }
        
        result = self.manager.place_limit_order("BTCUSDT", "SELL", 0.5, 66000.0)
        
        # Verify client was called with correct parameters
        self.mock_client.create_limit_order.assert_called_once_with(
            symbol="BTCUSDT",
            side="SELL",
            quantity=0.5,
            price=66000.0
        )
        
        # Verify structured response format
        self.assertTrue(result["success"])
        self.assertEqual(result["order_id"], "987654321")
        self.assertEqual(result["status"], "NEW")
        self.assertEqual(result["executed_qty"], "0.000")
        self.assertEqual(result["avg_price"], "0.0")

    def test_place_limit_order_validation_error(self):
        # Pass an invalid price (must be greater than 0)
        result = self.manager.place_limit_order("BTCUSDT", "SELL", 0.5, -100.0)
        
        # Client should not be called
        self.mock_client.create_limit_order.assert_not_called()
        
        # Verify failure response format
        self.assertFalse(result["success"])
        self.assertIn("Validation failed", result["error"])

    def test_place_limit_order_unexpected_error(self):
        # Setup client to raise a generic unexpected Exception
        self.mock_client.create_limit_order.side_effect = ValueError("Unexpected memory allocation failure")
        
        result = self.manager.place_limit_order("BTCUSDT", "SELL", 0.5, 66000.0)
        
        self.assertFalse(result["success"])
        self.assertIn("Unexpected system error occurred", result["error"])

if __name__ == "__main__":
    unittest.main()
