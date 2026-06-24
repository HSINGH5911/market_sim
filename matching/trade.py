"""
Represents a completed trade.

Stores buyer, seller, quantity, price, and timestamp
for each executed transaction.
"""

class Trade:

    def __init__(
        self,
        buyer,
        seller,
        quantity, 
        price,
        time,
        ticker
    ):
        self.buyer = buyer
        self.seller = seller
        self.quantity = quantity
        self.price = price
        self.time = time
        self.ticker = ticker
        

