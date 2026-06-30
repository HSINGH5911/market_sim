"""
Main entry point for the Market Simulator application.

Connects the Exchange, Matching Engine, Portfolios, Traders, Volatility, 
News Events, and Database. Runs the market simulation in a background thread 
while exposing the FastAPI endpoints to serve live market data.
"""

import threading
import time
import random
import uvicorn

# Import API components (sharing the same global exchange instance)
from api.main import app, exchange

# Import Market and Simulation components
from market.stock import Stock
from simulation.volatility import VolatilityModel
from simulation.news_events import News
from simulation.market_loop import MarketLoop

# Import Traders
from traders.market_maker import MarketMaker
from traders.retail import RetailTrader
from traders.institutional import InstitutionalTrader

def setup_market():
    print("Initializing Market Simulator components...")
    
    # 1. Define Stocks
    stocks_config = {
        "AAPL": 150.0,
        "MSFT": 250.0,
        "GOOG": 2800.0,
        "TSLA": 700.0,
        "NVDA": 220.0
    }
    
    stocks = []
    for symbol, price in stocks_config.items():
        stock = Stock(symbol=symbol, last_traded_price=price)
        exchange.add_stock(stock)
        stocks.append(stock)
        print(f"Added stock: {symbol} at initial price ${price:.2f}")

    # 2. Initialize Traders List
    traders = []

    # 3. Create and Register Market Maker
    mm = MarketMaker(
        trader_id=1,
        name="LiquidityProvider_MM",
        spread=2.0,
        quote_size=200,
        cash=10000000.0
    )
    # Seed Market Maker with inventory for each stock to facilitate trading
    for stock in stocks:
        mm.positions[stock.symbol] = 100000
    
    exchange.register_traders(mm)
    traders.append(mm)
    print(f"Registered Market Maker: {mm.name} (Cash: ${mm.cash:,.2f})")

    # 4. Create and Register Retail Traders (2 per stock)
    retail_id = 10
    for stock in stocks:
        for i in range(1, 3):
            rt = RetailTrader(
                trader_id=retail_id,
                name=f"Retail_{stock.symbol}_{i}",
                ticker=stock.symbol,
                cash=100000.0
            )
            # Seed retail traders with some shares to enable selling
            rt.positions[stock.symbol] = 1000
            exchange.register_traders(rt)
            traders.append(rt)
            retail_id += 1
            print(f"Registered Retail Trader: {rt.name} (Cash: ${rt.cash:,.2f})")

    # 5. Create and Register Institutional Traders (1 per stock)
    inst_id = 20
    for stock in stocks:
        it = InstitutionalTrader(
            trader_id=inst_id,
            name=f"Institution_{stock.symbol}",
            ticker=stock.symbol,
            cash=5000000.0
        )
        # Seed institutional traders with substantial shares
        it.positions[stock.symbol] = 50000
        exchange.register_traders(it)
        traders.append(it)
        inst_id += 1
        print(f"Registered Institutional Trader: {it.name} (Cash: ${it.cash:,.2f})")

    # 6. Setup Volatility and News models
    volatility_model = VolatilityModel(mode="LOW")
    news_generator = News(headline="Market opens normally.", sentiment=0.0)

    # 7. Initialize the Simulation Loop
    market_loop = MarketLoop(
        exchange=exchange,
        traders=traders,
        volatility_model=volatility_model,
        news=news_generator,
        max_ticks=1000000
    )
    
    return market_loop

def run_simulation(market_loop):
    print("Starting background simulation loop...")
    tick_delay = 1.0  # seconds between ticks
    
    while True:
        try:
            market_loop.advance_tick()
            time.sleep(tick_delay)
        except Exception as e:
            print(f"Error during simulation tick: {e}")
            time.sleep(2.0)

def main():
    # Setup database connection verification (ensures schema exists on startup)
    try:
        from database.db import get_connection
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
        tables = [r[0] for r in cur.fetchall()]
        print(f"Database connection verified. Tables present: {tables}")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Warning: Database setup verification failed: {e}")
        print("Please ensure PostgreSQL is running and database 'exchange_sim' exists.")

    # Initialize simulation components
    market_loop = setup_market()

    # Start simulation loop in a background daemon thread
    sim_thread = threading.Thread(target=run_simulation, args=(market_loop,), daemon=True)
    sim_thread.start()

    # Run the FastAPI server in the main thread
    print("Starting FastAPI API server...")
    uvicorn.run(app, host="127.0.0.1", port=8000)

if __name__ == "__main__":
    main()
