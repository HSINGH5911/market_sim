"""
Controls the simulation timeline.

Advances the market one step at a time, processes trader actions,
and updates prices and portfolios.
"""
from traders.market_maker import MarketMaker

class MarketLoop:
    def __init__(
        self,
        exchange,
        traders,
        max_ticks=1000
    ):
        self.exchange = exchange
        self.traders = traders
        self.max_ticks = max_ticks
        self.current_tick = 0
    
    def run(self):

        while self.current_tick < self.max_ticks:
            self.advance_tick()
        
        print("sim complete")
    
    def advance_tick(self):

        self.current_tick += 1

        self.generate_trader_actions()

        self.process_market()

    def generate_trader_actions(self, stock):

        for trader in self.traders:
            if isinstance(trader, MarketMaker):
                orders = trader.update_quotes(stock)

                for order in orders:
                    self.exchange.submit_order(order)
            else:
                order = trader.generate_order(stock)

                if order:
                    self.exchange.submit_order(order)


            if order is not None:
                self.exchange.process_orders()
