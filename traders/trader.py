"""
Base trader class.

Defines common functionality such as cash balances,
share holdings, order placement, and portfolio updates.
"""

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
        self.trade_hostory = []

    def place_order(self, order):
        pass

    def cancel_order(self, order):
        pass

    def update_position(self, trade):
        pass

    def portfolio_value(self, prices):
        pass
