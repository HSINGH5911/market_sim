"""
Base trader class.

Defines common functionality such as cash balances,
share holdings, order placement, and portfolio updates.
"""

import random

from market.exchange import Exchange

class Trader:

    def __init__(
        self,
        trader_id: int,
        name: str,
        cash: float = 100000
    ):
        self.trader_id = trader_id
        self.name = name
        self.cash = cash

        self.positions = {}
        self.open_orders = []
        self.trade_history = []

    def place_order(self, order):
        pass

    def cancel_order(self, order):
        pass

    def update_position(self, trade):
        ticker_price = trade.price
        ticker_name = trade.ticker
        ticker_quantity = trade.quantity

        trade_value = ticker_price * ticker_quantity

        if self.trader_id == trade.buyer:
            if trade_value > self.cash:
                raise ValueError("Not enough money")

            self.cash -= trade_value

            if ticker_name not in self.positions:
                self.positions[ticker_name] = 0
            
            self.positions[ticker_name] += ticker_quantity

        elif self.trader_id == trade.seller:
            if ticker_name not in self.positions:
                raise ValueError("No shares owned")

            if self.positions[ticker_name] < ticker_quantity:
                raise ValueError("Not enough shares")
            
            self.cash += trade_value

            if ticker_quantity == self.positions[ticker_name]:
                self.positions.pop(ticker_name)
            else:
                self.positions[ticker_name] -= ticker_quantity

    def portfolio_value(self, prices):
        total = self.cash

        for ticker, shares in self.positions.items():
            total += shares * prices[ticker]
        
        return total

    def generate_order(self, stocks, volatility_model):
       pass