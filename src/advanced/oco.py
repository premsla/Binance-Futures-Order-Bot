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


def place_oco_order(client: Client, symbol: str, side: str, quantity: float, stop_price: float, stop_limit_price: float, take_profit_price: float, logger):
    # Validate inputs
    if quantity <= 0 or stop_price <= 0 or stop_limit_price <= 0 or take_profit_price <= 0:
        raise ValueError('All prices and quantity must be positive')
    symbol = symbol.upper()
    side = side.upper()
    # Determine opposite side for OCO legs
    if side == 'BUY':
        tp_side = 'SELL'
        sl_side = 'SELL'
    else:
        tp_side = 'BUY'
        sl_side = 'BUY'
    try:
        # Take Profit Limit Order
        tp_order = client.futures_create_order(
            symbol=symbol,
            side=tp_side,
            type='TAKE_PROFIT',
            timeInForce='GTC',
            quantity=quantity,
            price=take_profit_price,
            stopPrice=take_profit_price
        )
        logger.info(f"Take-profit order placed: {tp_order}")
        print(tp_order)
        # Stop Market Order
        sl_order = client.futures_create_order(
            symbol=symbol,
            side=sl_side,
            type='STOP_MARKET',
            stopPrice=stop_price,
            closePosition=False,
            quantity=quantity
        )
        logger.info(f"Stop-market order placed: {sl_order}")
        print(sl_order)
    except (BinanceAPIException, ValueError) as e:
        logger.error(f"Error placing OCO orders: {e}")
        print(f"Error: {e}")


def main():
    parser = argparse.ArgumentParser(description='Place an OCO (take-profit and stop-loss) order')
    parser.add_argument('symbol', type=str, help='Trading pair symbol')
    parser.add_argument('side', type=str, choices=['BUY', 'SELL'], help='Initial order side')
    parser.add_argument('quantity', type=float, help='Quantity to trade')
    parser.add_argument('take_profit_price', type=float, help='Take profit price')
    parser.add_argument('stop_price', type=float, help='Stop trigger price')
    args = parser.parse_args()

    api_key = os.getenv('BINANCE_API_KEY')
    api_secret = os.getenv('BINANCE_API_SECRET')
    if not api_key or not api_secret:
        print("Error: Set BINANCE_API_KEY and BINANCE_API_SECRET environment variables.")
        exit(1)

    logger = setup_logger()
    client = Client(api_key, api_secret)
    place_oco_order(client, args.symbol, args.side, args.quantity, args.stop_price, args.stop_price, args.take_profit_price, logger)

if __name__ == '__main__':
    main()
