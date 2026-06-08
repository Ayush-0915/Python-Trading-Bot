import unittest
from bot.validators import (
    validate_symbol,
    validate_side,
    validate_order_type,
    validate_quantity,
    validate_price,
    ValidationError,
    InvalidSymbolError,
    InvalidSideError,
    InvalidOrderTypeError,
    InvalidQuantityError,
    InvalidPriceError
)

class TestValidators(unittest.TestCase):
    def test_validate_symbol_valid(self):
        self.assertEqual(validate_symbol("BTCUSDT"), "BTCUSDT")
        self.assertEqual(validate_symbol("ethusdt"), "ETHUSDT")
        self.assertEqual(validate_symbol("  solusdt  "), "SOLUSDT")
        self.assertEqual(validate_symbol("ADA1000"), "ADA1000")

    def test_validate_symbol_invalid(self):
        with self.assertRaises(InvalidSymbolError):
            validate_symbol(None)
        with self.assertRaises(InvalidSymbolError):
            validate_symbol("")
        with self.assertRaises(InvalidSymbolError):
            validate_symbol("   ")
        with self.assertRaises(InvalidSymbolError):
            validate_symbol("BTC-USDT")  # special character
        with self.assertRaises(InvalidSymbolError):
            validate_symbol("A")  # too short
        with self.assertRaises(InvalidSymbolError):
            validate_symbol("A" * 21)  # too long

    def test_validate_side_valid(self):
        self.assertEqual(validate_side("BUY"), "BUY")
        self.assertEqual(validate_side("sell"), "SELL")
        self.assertEqual(validate_side("  Buy  "), "BUY")

    def test_validate_side_invalid(self):
        with self.assertRaises(InvalidSideError):
            validate_side(None)
        with self.assertRaises(InvalidSideError):
            validate_side("HOLD")
        with self.assertRaises(InvalidSideError):
            validate_side("123")

    def test_validate_order_type_valid(self):
        self.assertEqual(validate_order_type("LIMIT"), "LIMIT")
        self.assertEqual(validate_order_type("market"), "MARKET")
        self.assertEqual(validate_order_type("  Limit  "), "LIMIT")

    def test_validate_order_type_invalid(self):
        with self.assertRaises(InvalidOrderTypeError):
            validate_order_type(None)
        with self.assertRaises(InvalidOrderTypeError):
            validate_order_type("STOP_LOSS")

    def test_validate_quantity_valid(self):
        self.assertEqual(validate_quantity(10), 10.0)
        self.assertEqual(validate_quantity(0.001), 0.001)
        self.assertEqual(validate_quantity("0.5"), 0.5)

    def test_validate_quantity_invalid(self):
        with self.assertRaises(InvalidQuantityError):
            validate_quantity(None)
        with self.assertRaises(InvalidQuantityError):
            validate_quantity(0)
        with self.assertRaises(InvalidQuantityError):
            validate_quantity(-1.5)
        with self.assertRaises(InvalidQuantityError):
            validate_quantity("abc")

    def test_validate_price_valid(self):
        self.assertEqual(validate_price(100.5, "LIMIT"), 100.5)
        self.assertEqual(validate_price("25000", "LIMIT"), 25000.0)
        self.assertIsNone(validate_price(None, "MARKET"))
        self.assertIsNone(validate_price("", "MARKET"))

    def test_validate_price_invalid(self):
        with self.assertRaises(InvalidPriceError):
            validate_price(None, "LIMIT")
        with self.assertRaises(InvalidPriceError):
            validate_price("", "LIMIT")
        with self.assertRaises(InvalidPriceError):
            validate_price(0, "LIMIT")
        with self.assertRaises(InvalidPriceError):
            validate_price(-50.0, "LIMIT")
        with self.assertRaises(InvalidPriceError):
            validate_price("abc", "LIMIT")

if __name__ == "__main__":
    unittest.main()
