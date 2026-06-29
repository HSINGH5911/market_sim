from database.db import get_connection


def save_trader(trader):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO traders
        (
            trader_id,
            name,
            cash
        )
        VALUES (%s, %s, %s)
        """,
        (
            trader.trader_id,
            trader.name,
            trader.cash
        )
    )

    conn.commit()

    cur.close()
    conn.close()

def save_trade(trade):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO trades
        (
            buyer_id,
            seller_id,
            ticker,
            quantity,
            price,
            trade_time
        )
        VALUES (%s,%s,%s,%s,%s,%s)
        """,
        (
            trade.buyer,
            trade.seller,
            trade.ticker,
            trade.quantity,
            trade.price,
            trade.time
        )
    )

    conn.commit()

    cur.close()
    conn.close()

def save_position(
    trader_id,
    ticker,
    shares
):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO positions
        (
            trader_id,
            ticker,
            shares
        )
        VALUES (%s,%s,%s)
        """,
        (
            trader_id,
            ticker,
            shares
        )
    )

    conn.commit()

    cur.close()
    conn.close()

