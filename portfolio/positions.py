"""
Tracks stock ownership.

Maintains share quantities, average cost basis,
and unrealized profit or loss for each holding.
"""

class Position:
    def __init__(
        self,
        ticker,
        shares = 0
    ):
        self.ticker = ticker
        self.shares = shares
    
    def average_cost(self, ticker, shares):
        pass

    def unrealized_pnl(self, ticker, shares):
        pass

    