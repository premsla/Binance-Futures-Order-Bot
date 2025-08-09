#!/usr/bin/env python3
"""
Stop-Limit order CLI for Binance USDT-M Futures.
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

def place_stop_limit_order(client: Client, symbol: str, side: str, quantity: float, stop_price: float, limit_price: float, logger):
    # Validate inputs
    if quantity <= 0 or stop_price <= 0 or limit_price <= 0:
        raise ValueError('Quantity, stop_price, and limit_price must be positive')
    symbol = symbol.upper()
    try:
        order = client.futures_create_order(
            symbol=symbol,
            side=side.upper(),
            type='STOP',
            timeInForce='GTC',
            quantity=quantity,
            price=limit_price,
            stopPrice=stop_price
        )
        logger.info(f"Stop-limit order placed: {order}")
        print(order)
    except (BinanceAPIException, ValueError) as e:
        logger.error(f"Error placing stop-limit order: {e}")
        print(f"Error: {e}")

def main():
    parser = argparse.ArgumentParser(description='Place a stop-limit order')
    parser.add_argument('symbol', type=str, help='Trading pair symbol')
    parser.add_argument('side', type=str, choices=['BUY', 'SELL'], help='Order side')
    parser.add_argument('quantity', type=float, help='Quantity to trade')
    parser.add_argument('stop_price', type=float, help='Stop trigger price')
    parser.add_argument('limit_price', type=float, help='Limit order price after trigger')
    args = parser.parse_args()

    api_key = os.getenv('BINANCE_API_KEY')
    api_secret = os.getenv('BINANCE_API_SECRET')
    if not api_key or not api_secret:
        print("Error: Set BINANCE_API_KEY and BINANCE_API_SECRET environment variables.")
        exit(1)

    logger = setup_logger()
    client = Client(api_key, api_secret)
    place_stop_limit_order(client, args.symbol, args.side, args.quantity, args.stop_price, args.limit_price, logger)

if __name__ == '__main__':
    main()
