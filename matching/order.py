"""

Creates order for stock
Saves the trader, side its on, quantity, and price
"""

class Order:

    def __init__(
      self,
      trader_ID,
      side,
      ticker,
      quantity,
      price      
    ):
        self.trader_ID = trader_ID
        self.side = side.upper()
        self.ticker = ticker.upper()
        self.quantity = quantity
        self.price = price