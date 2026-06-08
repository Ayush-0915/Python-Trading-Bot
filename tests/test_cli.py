import unittest
from unittest.mock import patch, MagicMock
import sys
from io import StringIO
from cli import main

class TestCLI(unittest.TestCase):
    
    @patch("cli.OrderManager")
    @patch("sys.argv", ["cli.py", "--symbol", "BTCUSDT", "--side", "BUY", "--type", "MARKET", "--quantity", "0.01"])
    def test_cli_market_order_success(self, mock_order_manager_class):
        # Mock the OrderManager instance and its response
        mock_manager = MagicMock()
        mock_order_manager_class.return_value = mock_manager
        mock_manager.place_market_order.return_value = {
            "success": True,
            "order_id": "123456789",
            "status": "FILLED",
            "executed_qty": "0.01",
            "avg_price": "104500"
        }
        
        # Capture stdout
        captured_output = StringIO()
        sys.stdout = captured_output
        
        try:
            main()
        except SystemExit:
            pass
        finally:
            sys.stdout = sys.__stdout__
            
        output = captured_output.getvalue()
        
        # Verify call parameters
        mock_manager.place_market_order.assert_called_once_with(
            symbol="BTCUSDT",
            side="BUY",
            quantity=0.01
        )
        
        # Verify terminal output sections
        self.assertIn("========== ORDER REQUEST ==========", output)
        self.assertIn("Symbol: BTCUSDT", output)
        self.assertIn("Side: BUY", output)
        self.assertIn("Type: MARKET", output)
        self.assertIn("Quantity: 0.01", output)
        self.assertIn("========== ORDER RESPONSE ==========", output)
        self.assertIn("Order ID: 123456789", output)
        self.assertIn("Status: FILLED", output)
        self.assertIn("Executed Qty: 0.01", output)
        self.assertIn("Avg Price: 104500", output)
        self.assertIn("SUCCESS: Order placed successfully.", output)

    @patch("cli.OrderManager")
    @patch("sys.argv", ["cli.py", "--symbol", "BTCUSDT", "--side", "SELL", "--type", "LIMIT", "--quantity", "0.05", "--price", "105000"])
    def test_cli_limit_order_success(self, mock_order_manager_class):
        mock_manager = MagicMock()
        mock_order_manager_class.return_value = mock_manager
        mock_manager.place_limit_order.return_value = {
            "success": True,
            "order_id": "987654321",
            "status": "NEW",
            "executed_qty": "0.0",
            "avg_price": "0.0"
        }
        
        captured_output = StringIO()
        sys.stdout = captured_output
        
        try:
            main()
        except SystemExit:
            pass
        finally:
            sys.stdout = sys.__stdout__
            
        output = captured_output.getvalue()
        
        mock_manager.place_limit_order.assert_called_once_with(
            symbol="BTCUSDT",
            side="SELL",
            quantity=0.05,
            price=105000.0
        )
        
        self.assertIn("========== ORDER REQUEST ==========", output)
        self.assertIn("Price: 105000.0", output)
        self.assertIn("========== ORDER RESPONSE ==========", output)
        self.assertIn("Order ID: 987654321", output)
        self.assertIn("SUCCESS: Order placed successfully.", output)

    @patch("cli.OrderManager")
    @patch("sys.argv", ["cli.py", "--symbol", "BTCUSDT", "--side", "BUY", "--type", "MARKET", "--quantity", "0.01"])
    def test_cli_order_failure(self, mock_order_manager_class):
        mock_manager = MagicMock()
        mock_order_manager_class.return_value = mock_manager
        mock_manager.place_market_order.return_value = {
            "success": False,
            "error": "Validation failed for quantity."
        }
        
        captured_output = StringIO()
        sys.stdout = captured_output
        
        with self.assertRaises(SystemExit) as cm:
            main()
            
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        
        # Exited with non-zero code
        self.assertEqual(cm.exception.code, 1)
        self.assertIn("FAILED: Validation failed for quantity.", output)

    @patch("sys.argv", ["cli.py", "--symbol", "BTCUSDT", "--side", "BUY", "--type", "LIMIT", "--quantity", "0.01"])
    @patch("sys.stderr", new_callable=StringIO)
    def test_cli_missing_price_for_limit(self, mock_stderr):
        # When --price is missing for a LIMIT order, argparse should exit with an error.
        with self.assertRaises(SystemExit) as cm:
            main()
            
        self.assertEqual(cm.exception.code, 2)
        self.assertIn("Price is required when order type is LIMIT", mock_stderr.getvalue())

if __name__ == "__main__":
    unittest.main()
