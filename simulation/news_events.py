"""
Generates market-moving news events.

Creates positive and negative events that influence
trader behavior and market sentiment.
"""

import random

class News:

    def __init__(
        self,
        headline,
        sentiment
    ):
        self.headline = headline
        self.sentiment = sentiment

    @staticmethod
    def generate_news():

        news = [
            
            (
                "Strong earnings report",
                0.8
            ),

            (
                "New product launch exceeds expectations",
                0.6
            ),

            (
                "Analysts upgrade outlook",
                0.4
            ),

            (
                "No major developments reported",
                0.0
            ),

            (
                "Economic uncertainty increases",
                -0.4
            ),

            (
                "Company misses earning expectations",
                -0.6
            ),

            (
                "Major regulatory investigation announced",
                -0.8
            ),

        ]

        headline, sentiment = random.choice(news)

        return News(
            headline,
            sentiment
        )
    
    