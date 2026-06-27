"""
Represents a stock being traded.

Tracks ticker symbol, last traded price, volume,
and other market statistics.
"""

class Stock:
    
    def __init__(
        self,
        symbol,
        last_traded_price,
        volume=0,
        volatility = "LOW",
    ):
        self.symbol = symbol
        self.last_traded_price = last_traded_price
        self.volume = volume
        self.volatility = volatility

        self.open_price = last_traded_price
        self.high_price = last_traded_price
        self.low_price = last_traded_price

        self.price_history = [last_traded_price]
