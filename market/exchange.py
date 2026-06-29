"""
Coordinates trading activity.

Receives orders from traders, routes them to the matching engine,
and maintains market-wide state.
"""

from matching.order_book import OrderBook
from matching.matching_engine import Matching_Engine
from database.repository import save_trade

class Exchange:
    def __init__(self):
        self.stocks = {}
        self.order_books = {}
        self.matching_engines = {}
        self.trade_histories = {}
    
    def add_stock(self, stock):
        symbol = stock.symbol

        self.stocks[symbol] = stock
        self.order_books[symbol] = OrderBook()
        self.trade_histories[symbol] = []
        self.matching_engines[symbol] = Matching_Engine(
            self.order_books[symbol],
            stock
        )

    def submit_order(self, order):
        self.order_books[
            order.ticker
        ].add_order(order)
    
    def process_orders(self):

        for ticker, order_book in self.order_books.items():
            engine = self.matching_engines[ticker]

            while (
                order_book.bids
                and order_book.asks
                and order_book.bids[0].price >= order_book.asks[0].price
            ):
                trade = engine.execute_trade()
                self.trade_histories[ticker].append(trade)
                save_trade(trade)

    def get_last_price(self, stock):
        
        if stock in self.stocks:
            return self.stocks.get(stock).last_traded_price
        
        raise ValueError ("Trader does not own stock " + stock)
    
    def get_volume(self, stock):
        return self.stocks.get(stock).volume
    
    def get_trade_history(self, stock):
        return self.trade_histories[stock.symbol]
    
    