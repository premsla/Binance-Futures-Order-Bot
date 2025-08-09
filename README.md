# Binance USDT-M Futures Order Bot

## Overview
A CLI-based trading bot for Binance USDT-M Futures supporting:
- Market Orders
- Limit Orders
- Stop-Limit Orders
- OCO (One-Cancels-the-Other)
- TWAP (Time-Weighted Average Price)
- Grid Strategy

## Installation
1. Clone the repo:
```bash
git clone <your_repo_url> OrderBot
cd OrderBot
```
2. Install dependencies:
```bash
pip install python-binance
```
3. Set environment variables:
```bash
export BINANCE_API_KEY="<your_api_key>"
export BINANCE_API_SECRET="<your_api_secret>"
```
(On Windows PS use `$Env:BINANCE_API_KEY = "..."`)

## Usage
All scripts are in `src/`. Run via Python:

### Market Order
```bash
python src/market_orders.py BTCUSDT BUY 0.01
```

### Limit Order
```bash
python src/limit_orders.py BTCUSDT SELL 0.01 30000
```

### Stop-Limit Order
```bash
python src/advanced/stop_limit.py BTCUSDT BUY 0.01 29000 29500
```

### OCO Order
```bash
python src/advanced/oco.py BTCUSDT BUY 0.01 35000 34000
```

### TWAP Strategy
```bash
python src/advanced/twap.py BTCUSDT SELL 0.1 3600 6
```

### Grid Strategy
```bash
python src/advanced/grid.py BTCUSDT BUY 0.01 28000 30000 5
```

## Logging
All actions and errors are logged to `bot.log` in project root.

## Report
See `report.pdf` for analysis, screenshots, and evaluation.

## License
MIT License
