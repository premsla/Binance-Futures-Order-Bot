#!/usr/bin/env python3
"""
Grid strategy CLI for Binance USDT-M Futures.
"""

import os
import argparse
import logging
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

def execute_grid(client: Client, symbol: str, side: str, quantity: float, price_low: float, price_high: float, grid_count: int, logger):
    # Validate inputs
    if quantity <= 0 or price_low <= 0 or price_high <= price_low or grid_count <= 1:
        raise ValueError('Ensure quantity >0, price_high > price_low, grid_count >1')
    symbol = symbol.upper()
    side = side.upper()
    step = (price_high - price_low) / (grid_count - 1)
    for i in range(grid_count):
        price = round(price_low + step * i, 8)
        try:
            order = client.futures_create_order(
                symbol=symbol,
                side=side,
                type='LIMIT',
                timeInForce='GTC',
                quantity=quantity,
                price=price
            )
            logger.info(f"Grid order {i+1}/{grid_count} placed at {price}: {order}")
            print(order)
        except BinanceAPIException as e:
            logger.error(f"Error placing grid order at {price}: {e}")
            print(f"Error: {e}")

def main():
    parser = argparse.ArgumentParser(description='Execute grid strategy')
    parser.add_argument('symbol', type=str, help='Trading pair symbol')
    parser.add_argument('side', type=str, choices=['BUY', 'SELL'], help='Order side for grid')
    parser.add_argument('quantity', type=float, help='Quantity per order')
    parser.add_argument('price_low', type=float, help='Lower price bound')
    parser.add_argument('price_high', type=float, help='Upper price bound')
    parser.add_argument('grid_count', type=int, help='Number of grid levels')
    args = parser.parse_args()

    api_key = os.getenv('BINANCE_API_KEY')
    api_secret = os.getenv('BINANCE_API_SECRET')
    if not api_key or not api_secret:
        print("Error: Set BINANCE_API_KEY and BINANCE_API_SECRET environment variables.")
        exit(1)

    logger = setup_logger()
    client = Client(api_key, api_secret)
    execute_grid(client, args.symbol, args.side, args.quantity, args.price_low, args.price_high, args.grid_count, logger)

if __name__ == '__main__':
    main()
