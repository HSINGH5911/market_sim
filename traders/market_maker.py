"""
Provides liquidity to the market.

Continuously places buy and sell orders around
the current market price to profit from the spread.
"""

from traders.trader import Trader
from matching.order import Order
from simulation.volatility import VolatilityModel
from simulation.news_events import News

class MarketMaker(Trader):
    
    def __init__(
        self,
        trader_id,
        name,
        spread=2,
        quote_size=100,
        cash=1000000
    ):
        super().__init__(
            trader_id,
            name,
            cash
        )

        self.spread = spread
        self.quote_size = quote_size

    def generate_quotes(self, stock, news=None):

        market_price = stock.last_traded_price

        if news:
            self.spread = 2 + abs(news.sentiment) * 5
        
        spread_adjustment = abs(VolatilityModel.get_price_offset()) + self.spread
        bid_price = market_price - (spread_adjustment)
        ask_price = market_price + (spread_adjustment)

        bid_order = Order(
            self.trader_id,
            "BUY",
            stock.symbol,
            self.quote_size,
            bid_price
        )

        ask_order = Order(
            self.trader_id,
            "SELL",
            stock.symbol,
            self.quote_size,
            ask_price
        )
    
        return bid_order, ask_order

    def update_quotes(self, stock, news=None):

        self.open_orders.clear()

        bid_order, ask_order = self.generate_quotes(stock, news)

        self.open_orders.append(bid_order)
        self.open_orders.append(ask_order)

        return [bid_order, ask_order]