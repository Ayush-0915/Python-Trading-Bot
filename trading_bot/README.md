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

---

## Future Modules

As the project expands, the following modules will be introduced:

* **`bot/client.py`**: Handles initialization and connection to the Binance Futures API client.
* **`bot/orders.py`**: Logic for order creation, execution, and tracking.
* **`bot/validators.py`**: Validation logic for inputs, balances, trade sizes, and parameters.
* **`bot/logging_config.py`**: Logging setup to write events and errors to the `logs/` directory.
