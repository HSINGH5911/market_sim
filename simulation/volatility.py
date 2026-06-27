"""
Models market volatility.

Applies randomness and market fluctuations
to create realistic price movement.
"""

import random

class VolatilityModel:


    def __init__(
        self,
        mode = "LOW"
    ):
        self.mode = mode
    
    def get_price_offset(self):

        if self.mode == "LOW":
            return random.randint(-1, 1)
        
        return random.randint(-10, 10)

    def get_order_size_multiplier(self):
        
        if self.mode == "LOW":
            return random.uniform(0.8, 1.2)

        return random.uniform(0.5, 2.0)
    
    