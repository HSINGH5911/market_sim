"""

Creates order for stock
Saves the trader, side its on, quantity, and price
"""

class Order:

    def __init__(
      self,
      trader_id,
      side,
      ticker,
      quantity,
      price      
    ):
        self.trader_id = trader_id
        self.side = side.upper()
        self.ticker = ticker.upper()
        self.quantity = quantity
        self.price = price