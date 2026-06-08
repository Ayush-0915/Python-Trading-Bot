"""
Centralized logging configuration for the Binance Futures Trading Bot.
Provides a reusable logger configured to log events only to logs/trading.log.
"""

import logging
import os

def setup_logger(name: str) -> logging.Logger:
    """
    Sets up and configures a logger that logs messages to logs/trading.log.
    
    Args:
        name: The name of the logger (typically __name__ of the calling module).
        
    Returns:
        logging.Logger: Configured logger instance.
    """
    # Define directories relative to this file's directory:
    # bot/logging_config.py -> bot/ -> trading_bot/
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    logs_dir = os.path.join(project_root, "logs")
    
    # Ensure the logs directory exists
    os.makedirs(logs_dir, exist_ok=True)
    
    log_file_path = os.path.join(logs_dir, "trading.log")
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Prevent propagation to the root logger to avoid printing to console
    logger.propagate = False
    
    # Check if handler is already added to avoid duplicate logging handlers
    if not logger.handlers:
        file_handler = logging.FileHandler(log_file_path, encoding="utf-8")
        file_handler.setLevel(logging.INFO)
        
        # Format: Timestamp | Level | Module | Message
        # Example: 2026-06-08 12:30:15 | INFO | client | Connected to Binance Futures Testnet
        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
    return logger
