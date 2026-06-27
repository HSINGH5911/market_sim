"""
Controls the simulation timeline.

Advances the market one step at a time, processes trader actions,
and updates prices and portfolios.
"""

import random

from traders.market_maker import MarketMaker
from simulation.volatility import VolatilityModel

class MarketLoop:
    def __init__(
        self,
        exchange,
        traders,
        volatility_model,
        max_ticks=1000
    ):
        self.exchange = exchange
        self.traders = traders
        self.volatility_model = volatility_model
        self.max_ticks = max_ticks
        self.current_tick = 0
    
    def run(self):

        while self.current_tick < self.max_ticks:
            self.advance_tick()
        
        print("sim complete")
    
    def advance_tick(self):

        self.current_tick += 1

        self.generate_trader_actions()

        self.exchange.process_orders()

        if random.random < 0.01:

            if self.volatility_model.mode == "LOW":
                self.volatility_model.mode = "HIGH"
            
            else:
                self.volatility_model.mode = "LOW"

    def generate_trader_actions(self):
        
        for trader in self.traders:
            stock = self.exchange.stock

            if isinstance(trader, MarketMaker):
                orders = trader.update_quotes(stock)

                for order in orders:
                    self.exchange.submit_order(order)
            
            else:
                order = trader.generate_order(stock, self.volatility_model)

                if order:
                    self.exchange.submit_order(order)

