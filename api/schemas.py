"""
API endpoints for external access.

Allows users or front-end applications to submit orders,
view prices, and retrieve market data.
"""

from pydantic import BaseModel


class OrderRequest(BaseModel):

    trader_id: int
    ticker: str
    side: str
    quantity: int
    price: float
