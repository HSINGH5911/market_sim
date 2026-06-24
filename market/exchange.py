"""
Coordinates trading activity.

Receives orders from traders, routes them to the matching engine,
and maintains market-wide state.
"""

class Exchange:
    def __init__(
        self,
        stock,
        order_book,
        matching_engine
    ):
        self.stock = stock
        self.order_book = order_book
        self.matching_engine = matching_engine
    
    def submit_order(self, order):
        self.order_book.add_order(order)
    
    def process_orders(self):
        while (
            self.order_book.bids
            and self.order_book.asks
            and self.order_book.bids[0].price >= self.order_book.asks[0].price
        ):
            trade = self.matching_engine.execute_trade()
            self.trade_history.append(trade)

    def get_last_price(self):
        return self.stock.last_price
    
    def get_volume(self):
        return self.stock.volume
    
    