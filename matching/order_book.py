"""
Maintains buy and sell orders for a stock.

Stores bids and asks, keeps them sorted by price priority,
and provides access to the best bid and best ask.
"""

class OrderBook:

    def __init__(self):
        self.bids = []
        self.asks = []
        self.price = 0

    def add_order(self, order):
        if order.side == "BUY":
            self.bids.append(order)
            self.bids.sort(key=lambda o: o.price, reverse=True)
        else:
            self.asks.append(order)
            self.asks.sort(key=lambda o: o.price)

    def remove_order(self, order):
        if order.side == "BUY":
            self.bids.remove(order)
        else:
            self.asks.remove(order)

    def best_bid(self):
        if not self.bids:
            return None

        self.bids.sort(key=lambda o: o.price, reverse=True)
        self.price = self.bids[0]
        return self.bids[0]

    def best_ask(self):
        if not self.asks:
            return None

        self.asks.sort(key=lambda o: o.price)
        self.price = self.asks[0]
        return self.asks[0]