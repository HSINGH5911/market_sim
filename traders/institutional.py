"""
Represents large institutional investors.

Places large orders capable of moving market prices
and creating significant market impact.
"""

import random

from traders.trader import Trader
from matching.order import Order
from simulation.volatility import VolatilityModel
from simulation.news_events import News

class InstitutionalTrader(Trader):

    def __init__(
        self,
        trader_id,
        name,
        ticker,
        cash=1000000
    ):
        super().__init__(
            trader_id,
            name,
            cash
        )

        self.ticker = ticker
        self.mode = random.choice(
            ["ACCUMULATE", "DISTRIBUTE"]
        )

    def position_size(self):
        return int(random.randint(500, 5000) + VolatilityModel.get_order_size_multiplier())

    def generate_order(self, stock, news=None):
        if news:
            if news.sentiment > 0.5:
                self.mode = "ACCUMULATE"
            elif news.sentiment < -0.5:
                self.mode = "DISTRIBUTE"
        
        if self.mode == "ACCUMULATE":
            return self.generate_buy_order(stock)
        
        return self.generate_sell_order(stock)
    
    def generate_buy_order(self, stock):
        quantity = self.position_size()
        price = stock.last_traded_price + 1
        cost = quantity * price

        if cost > self.cash:
            return None
        
        return Order(
            self.trader_id,
            "BUY",
            stock.symbol,
            quantity,
            price
        )
    
    def generate_sell_order(self, stock):
        shares_owned = self.positions.get(stock.symbol, 0)

        if shares_owned <= 0:
            return None
        
        quantity = min(shares_owned, self.position_size())

        price = stock.last_traded_price - 1

        return Order(
            self.trader_id,
            "SELL",
            stock.symbol,
            quantity,
            price
        )