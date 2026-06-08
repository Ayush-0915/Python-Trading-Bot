# Binance Futures Testnet Trading Bot

A professional, modular cryptocurrency algorithmic trading bot designed to interface with the Binance Futures Testnet platform using Python.

## Project Overview

This project is a Binance Futures Testnet Trading Bot built in Python. It provides a robust, extensible framework for testing trading strategies, managing futures orders, and monitoring real-time market data in a safe, risk-free testnet environment.

---

## Prerequisites

Before setting up and running the bot, ensure you have the following requirements:

* **Python 3.10+** installed on your system.
* A **Binance Futures Testnet account**.
* **API Key** and **API Secret** from the Binance Futures Testnet interface.

---

## Installation

Follow these steps to clone the repository and set up your local development environment:

```bash
# Clone the repository (replace <repository_url> with the actual URL)
git clone <repository_url>
cd trading_bot

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# Windows (Command Prompt / PowerShell):
venv\Scripts\activate

# Linux/macOS:
source venv/bin/activate

# Install the required dependencies
pip install -r requirements.txt
```

---

## Environment Setup

The application uses environment variables to securely load API credentials without hardcoding them in the source code.

1. Copy the example configuration file:
   ```bash
   cp .env.example .env
   ```
2. Open the newly created `.env` file.
3. Add your Binance Futures Testnet API credentials:
   ```env
   BINANCE_API_KEY=your_actual_testnet_api_key
   BINANCE_API_SECRET=your_actual_testnet_api_secret
   ```

---

## Binance Futures Testnet

To create a testnet account and manage your credentials, visit the official testnet dashboard:

* **Testnet URL**: [https://testnet.binancefuture.com](https://testnet.binancefuture.com)

Here you can obtain virtual funds to safely test trading logic, order execution, and account management.

## Binance Client Layer

The Binance Client Layer is implemented in `bot/client.py` under the `BinanceClient` class. 

### Purpose & Features
* **Communication Interface**: Serves as the sole layer responsible for sending REST requests to the Binance Futures Testnet and returning raw API responses.
* **Exception Translation**: Catches library-level (`python-binance`), networking (`requests`), and timeout exceptions, translating them into descriptive, domain-specific exception classes (`MissingCredentialsError`, `InvalidCredentialsError`, `BinanceAPIError`, `BinanceNetworkError`, `BinanceTimeoutError`).
* **Connection Health**: Implements `ping()` and `get_server_time()` and checks endpoint connectivity.
* **Order Placement**: Supports raw order generation via `create_market_order()` and `create_limit_order()`.

---

## Input Validation Layer

The Input Validation Layer is implemented in `bot/validators.py` to check and sanitize user/CLI inputs before sending any requests to the Binance API.

### Validation Rules
* **Symbol**: Alphanumeric uppercase string (3-20 chars) (e.g. `BTCUSDT`). Normalizes input to uppercase.
* **Side**: Case-insensitive string matching `BUY` or `SELL`. Normalizes input to uppercase.
* **Order Type**: Case-insensitive string matching `MARKET` or `LIMIT`. Normalizes input to uppercase.
* **Quantity**: Must be numeric (or numeric string) and strictly greater than 0. Returns value as a `float`.
* **Price**: Required for `LIMIT` orders. Must be numeric and strictly greater than 0. Returns value as a `float`.

### Custom Exceptions
Provides localized exceptions subclassing `ValidationError`:
* `InvalidSymbolError`
* `InvalidSideError`
* `InvalidOrderTypeError`
* `InvalidQuantityError`
* `InvalidPriceError`

## Centralized Logging System

The logging configuration is implemented in `bot/logging_config.py` using Python's standard `logging` module.

### Features
* **File Logging Only**: Configured to log exclusively to `logs/trading.log` (automatically creates the `logs` folder if it doesn't exist).
* **Format**: `Timestamp | Level | Module | Message`
  * Example: `2026-06-08 12:30:15 | INFO | client | Connected to Binance Futures Testnet`
* **Log Levels**: Support for `INFO`, `WARNING`, and `ERROR` levels.
* **No Propagation / Console Print**: Setting `propagate = False` ensures console logs are suppressed, making file logs the sole record.

---

## Order Processing Layer

The Order Processing Layer is implemented in `bot/orders.py` under the `OrderManager` class. It manages coordination between validation, logging, and sending requests to the API client:
- **Validation**: Coordinates parsing of fields using the Input Validation Layer.
- **Pre-flight & Post-flight Logging**: Automatically records the intent of execution, responses from Binance Futures API, and details of any raised exception inside `logs/trading.log`.
- **Exception Boundary**: Safely maps internal exceptions (`ValidationError`, `BinanceClientError`, etc.) to structured JSON-like failure states.

---

## Command Line Interface (CLI)

The Command Line Interface (CLI) is implemented in `cli.py` to allow direct execution of orders from the terminal.

### Usage

Run the CLI using python with the virtual environment activated:

```bash
# Market Order
python cli.py --symbol <symbol> --side <side> --type MARKET --quantity <quantity>

# Limit Order
python cli.py --symbol <symbol> --side <side> --type LIMIT --quantity <quantity> --price <price>
```

### Examples

**Placing a Market Order:**
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01
```

**Placing a Limit Order:**
```bash
python cli.py --symbol BTCUSDT --side BUY --type LIMIT --quantity 0.01 --price 104500
```

