"""
Command Line Interface (CLI) for the Binance Futures Testnet Trading Bot.
Handles parameter parsing, validation coordination, and results formatting.
"""

import argparse
import sys
from dotenv import load_dotenv
from bot.orders import OrderManager

def main():
    # Load environment variables from .env file
    load_dotenv()

    parser = argparse.ArgumentParser(
        description="CLI Interface for Binance Futures Testnet Trading Bot."
    )
    parser.add_argument(
        "--symbol",
        required=True,
        help="Trading pair symbol (e.g., BTCUSDT)"
    )
    parser.add_argument(
        "--side",
        required=True,
        help="Order side (BUY or SELL)"
    )
    parser.add_argument(
        "--type",
        required=True,
        help="Order type (MARKET or LIMIT)"
    )
    parser.add_argument(
        "--quantity",
        required=True,
        type=float,
        help="Order quantity"
    )
    parser.add_argument(
        "--price",
        type=float,
        help="Order price (required for LIMIT orders)"
    )

    args = parser.parse_args()

    # Custom price check for LIMIT orders
    order_type = args.type.upper()
    if order_type == "LIMIT" and args.price is None:
        parser.error("Price is required when order type is LIMIT.")

    # 1. Print Order Request Summary
    print("========== ORDER REQUEST ==========")
    print(f"Symbol: {args.symbol.upper()}")
    print(f"Side: {args.side.upper()}")
    print(f"Type: {order_type}")
    print(f"Quantity: {args.quantity}")
    if order_type == "LIMIT":
        print(f"Price: {args.price}")
    print("==============")
    print()

    # 2. Instantiate OrderManager and call place order
    try:
        manager = OrderManager()
    except Exception as e:
        print(f"FAILED: Initialization error: {e}")
        sys.exit(1)

    if order_type == "MARKET":
        response = manager.place_market_order(
            symbol=args.symbol,
            side=args.side,
            quantity=args.quantity
        )
    elif order_type == "LIMIT":
        response = manager.place_limit_order(
            symbol=args.symbol,
            side=args.side,
            quantity=args.quantity,
            price=args.price
        )
    else:
        print(f"FAILED: Unsupported order type: {order_type}")
        sys.exit(1)

    # 3. Print Order Response Details and Success/Failure Message
    if response.get("success"):
        print("========== ORDER RESPONSE ==========")
        print(f"Order ID: {response.get('order_id')}")
        print(f"Status: {response.get('status')}")
        print(f"Executed Qty: {response.get('executed_qty')}")
        print(f"Avg Price: {response.get('avg_price')}")
        print("=================")
        print()
        print("SUCCESS: Order placed successfully.")
    else:
        print(f"FAILED: {response.get('error')}")
        sys.exit(1)

if __name__ == "__main__":
    main()
