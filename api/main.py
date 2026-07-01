from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from api.schemas import OrderRequest
from market.exchange import Exchange
from matching.order import Order

exchange = Exchange()

app = FastAPI(
    title="Exchange Simulator API"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5173", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/stocks")
def get_stocks():
    return [
        {
            "ticker": stock.symbol,
            "price": stock.last_traded_price,
            "volume": stock.volume
        }
        for stock in exchange.stocks.values()
    ]

@app.get("/orderbook/{ticker}")
def get_orderbook(ticker: str):
    book = exchange.order_books[ticker]

    return {
        "bids" : [
            vars(order)
            for order in book.bids
        ],
        "asks" : [
            vars(order)
            for order in book.asks
        ]
    }

@app.get("/trades/{ticker}")
def get_trades(ticker: str):
    return [
        vars(trade)
        for trade in exchange.trade_histories[ticker]
    ]

@app.post("/order")
def submit_order(request: OrderRequest):
    order = Order(
        request.trader_id,
        request.side,
        request.ticker,
        request.quantity,
        request.price
    )

    exchange.submit_order(order)

    exchange.process_orders()

    return {
        "message" : "order accepted"
    }

@app.get("/portfolio/{trader_id}")
def get_portfolio(trader_id: int):
    if trader_id not in exchange.traders:
        raise HTTPException(status_code=404, detail="Trader not found")
    trader = exchange.traders[trader_id]
 
    return {
        "cash": trader.cash,
        "positions": trader.positions
    }

@app.get("/")
def health():
    return {
        "status": "running"
    }