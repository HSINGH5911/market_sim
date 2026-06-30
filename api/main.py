from fastapi import FastAPI
from api.schemas import OrderRequest
from market.exchange import Exchange
from matching.order import Order

exchange = Exchange()

app = FastAPI(
    title="Exchange Simulator API"
)

@app.get("/stocks")
def get_stocks():
    return (
        {
            "ticker": stock.symbol,
            "price": stock.last_traded_price,
            "volume": stock.volume
        }

        for stock in exchange.stocks.values()
    )

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
    trader = exchange.traders[
        trader_id
    ]
 
    return {
        "cash": trader.cash,
        "positions": trader.positions
    }

@app.get("/")
def health():
    return {
        "status": "running"
    }