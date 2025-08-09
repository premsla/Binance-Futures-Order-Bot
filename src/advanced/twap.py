#!/usr/bin/env python3
"""
TWAP (Time-Weighted Average Price) CLI for Binance USDT-M Futures.
"""

import os
import argparse
import logging
import time
from binance.client import Client
from binance.exceptions import BinanceAPIException

def setup_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler('bot.log')
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

def execute_twap(client: Client, symbol: str, side: str, quantity: float, duration: int, intervals: int, logger):
    # Validate inputs
    if quantity <= 0 or duration <= 0 or intervals <= 0:
        raise ValueError('Quantity, duration, and intervals must be positive')
    symbol = symbol.upper()
    side = side.upper()
    chunk = quantity / intervals
    delay = duration / intervals
    for i in range(intervals):
        try:
            order = client.futures_create_order(
                symbol=symbol,
                side=side,
                type='MARKET',
                quantity=round(chunk, 8)
            )
            logger.info(f"TWAP chunk {i+1}/{intervals} placed: {order}")
            print(order)
        except BinanceAPIException as e:
            logger.error(f"Error in TWAP chunk {i+1}: {e}")
            print(f"Error: {e}")
        if i < intervals - 1:
            time.sleep(delay)

def main():
    parser = argparse.ArgumentParser(description='Execute TWAP strategy')
    parser.add_argument('symbol', type=str, help='Trading pair symbol')
    parser.add_argument('side', type=str, choices=['BUY', 'SELL'], help='Order side')
    parser.add_argument('quantity', type=float, help='Total quantity to trade')
    parser.add_argument('duration', type=int, help='Total duration in seconds')
    parser.add_argument('intervals', type=int, help='Number of intervals')
    args = parser.parse_args()

    api_key = os.getenv('BINANCE_API_KEY')
    api_secret = os.getenv('BINANCE_API_SECRET')
    if not api_key or not api_secret:
        print("Error: Set BINANCE_API_KEY and BINANCE_API_SECRET environment variables.")
        exit(1)

    logger = setup_logger()
    client = Client(api_key, api_secret)
    execute_twap(client, args.symbol, args.side, args.quantity, args.duration, args.intervals, logger)

if __name__ == '__main__':
    main()
