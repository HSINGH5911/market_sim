CREATE TABLE traders (
    trader_id INTEGER PRIMARY KEY,
    name VARCHAR(100),
    cash NUMERIC
);

CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    trader_id INTEGER,
    ticker VARCHAR(10),
    side VARCHAR(10),
    quantity INTEGER,
    price NUMERIC,
    created_at TIMESTAMP
);

CREATE TABLE trades(
    trade_id SERIAL PRIMARY KEY,
    buyer_id INTEGER,
    seller_id INTEGER,
    ticker VARCHAR(10),
    quantity INTEGER,
    price NUMERIC,
    trade_time TIMESTAMP
);

CREATE TABLE positions(
    position_id SERIAL PRIMARY KEY,
    trader_id INTEGER,
    ticker VARCHAR(10),
    shares INTEGER
);