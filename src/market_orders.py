import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
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

def place_market_order(client: Client, symbol: str, side: str, quantity: float, logger):
    # Validate inputs
    if quantity <= 0:
        raise ValueError('Quantity must be positive')
    symbol = symbol.upper()
    try:
        order = client.futures_create_order(
            symbol=symbol,
            side=side.upper(),
            type='MARKET',
            quantity=quantity
        )
        logger.info(f"Market order placed: {order}")
        print(order)
    except BinanceAPIException as e:
        logger.error(f"Error placing market order: {e}")
        print(f"Error: {e}")

def main():
    parser = argparse.ArgumentParser(description='Place a market order')
    parser.add_argument('symbol', type=str, help='Trading pair symbol')
    parser.add_argument('side', type=str, choices=['BUY', 'SELL'], help='Order side')
    parser.add_argument('quantity', type=float, help='Quantity to trade')
    args = parser.parse_args()

    api_key = os.getenv('BINANCE_API_KEY')
    api_secret = os.getenv('BINANCE_API_SECRET')
    if not api_key or not api_secret:
        print("Error: Set BINANCE_API_KEY and BINANCE_API_SECRET environment variables.")
        exit(1)

    logger = setup_logger()
    client = Client(api_key, api_secret)
    place_market_order(client, args.symbol, args.side, args.quantity, logger)

if __name__ == '__main__':
    main()
