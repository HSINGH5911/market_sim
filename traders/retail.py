"""
Represents individual retail investors.

Places relatively small orders using simple strategies
or random market behavior.
"""

import random

from traders.trader import Trader
from matching.order import Order
from simulation.volatility import VolatilityModel

class ReatilTrader(Trader):

    def __init__(
        self, 
        trader_id, 
        name, 
        ticker,
        cash = 100000
    ):
        super().__init__(
            trader_id, 
            name, 
            cash
        )

        self.ticker = ticker
    
    def generate_order(self):
        action = random.random()

        if action < 0.4:
            return self.generate_buy_order()
        elif action < 0.8:
            return self.generate_sell_order()
        
        return None

    def generate_buy_order(self, stock):
        quantity = self.position_size()

        price = stock.last_traded_price + random.randint(-2, 2)

        cost = quantity * price

        if cost > self.cash:
            return None
            # raise valerr later maybe
        
        return Order(
            self.trader_id,
            "BUY",
            stock.symbol,
            quantity,
            price
        )

    def generate_sell_order(self, stock):
        shares_owned = self.positions.get(
            stock.symbol,
            0
        )

        if shares_owned == 0:
            return None
            #raise valerr later maybe
        
        quantity = min(
            self.position_size(),
            shares_owned
        )

        price = stock.last_traded_price + VolatilityModel.get_price_offset()

        return Order(
            self.trader_id,
            "SELL",
            stock.symbol,
            quantity,
            price
        )

    def position_size(self):
        return random.randint(1, 25)
        # update to reflect actual stock prices. Im not buying 1 share of a $2 stock