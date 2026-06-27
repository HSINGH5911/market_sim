"""
Matches incoming buy and sell orders.

Executes trades whenever a bid price is greater than or equal
to an ask price and updates the order book accordingly.
"""

from matching.trade import Trade
import time

class Matching_Engine:

    def __init__(self, order_book, stock):
        self.order_book = order_book
        self.stock = stock
    
    def is_bid_greater_than_ask(self, bids, asks):
        return bids[0].price >= asks[0].price
    
    def execute_trade(self):
        best_bid = self.order_book.bids[0]
        best_ask = self.order_book.asks[0]

        quantity = min(
            best_bid.quantity,
            best_ask.quantity
        )

        trade_price = best_ask.price

        trade = Trade(
            buyer=best_bid.trader_id,
            seller=best_ask.trader_id,
            ticker=best_bid.ticker,
            quantity=quantity,
            price=trade_price,
            time=time.time()
        )

        self.stock.last_traded_price = trade_price
        self.stock.volume += quantity

        if quantity >= 1000:
            impact = quantity / 10000
            self.stock.last_traded_price += impact
        

        best_bid.quantity -= quantity
        best_ask.quantity -= quantity

        if best_bid.quantity == 0:
            self.order_book.bids.pop(0)

        if best_ask.quantity == 0:
            self.order_book.asks.pop(0)

        return trade


    
