"""
Models market volatility.

Applies randomness and market fluctuations
to create realistic price movement.
"""

import random

class VolatilityModel:
    _mode = "LOW"

    def __init__(
        self,
        mode = "LOW"
    ):
        VolatilityModel._mode = mode
    
    @property
    def mode(self):
        return VolatilityModel._mode

    @mode.setter
    def mode(self, value):
        VolatilityModel._mode = value
    
    @classmethod
    def get_price_offset(cls):
        if cls._mode == "LOW":
            return random.randint(-1, 1)
        
        return random.randint(-10, 10)

    @classmethod
    def get_order_size_multiplier(cls):
        if cls._mode == "LOW":
            return random.uniform(0.8, 1.2)

        return random.uniform(0.5, 2.0)
    
    