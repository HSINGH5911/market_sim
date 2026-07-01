import { useEffect, useState } from "react";
import {
  getStocks,
  getOrderbook,
  getTrades,
  getPortfolio,
  submitOrder,
} from "./api";

const defaultOrder = {
  trader_id: 1,
  ticker: "AAPL",
  side: "BUY",
  quantity: 100,
  price: 150,
};

const formatCurrency = (value) =>
  new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
  }).format(value);

export default function App() {
  const [stocks, setStocks] = useState([]);
  const [selectedTicker, setSelectedTicker] = useState("AAPL");
  const [orderbook, setOrderbook] = useState({ bids: [], asks: [] });
  const [trades, setTrades] = useState([]);
  const [portfolioId, setPortfolioId] = useState(1);
  const [portfolio, setPortfolio] = useState(null);
  const [orderForm, setOrderForm] = useState(defaultOrder);
  const [statusMessage, setStatusMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const [stockOptions, setStockOptions] = useState([]);

  const fetchStocks = async () => {
    try {
      const data = await getStocks();
      setStocks(data);
      const tickers = data.map((stock) => stock.ticker);
      setStockOptions(tickers);
      if (!tickers.includes(selectedTicker) && data.length > 0) {
        setSelectedTicker(data[0].ticker);
      }
    } catch (error) {
      console.error(error);
      setStatusMessage("Unable to load stocks. Is the backend running?");
    }
  };

  const fetchMarketData = async (ticker) => {
    if (!ticker) return;
    setLoading(true);
    try {
      const [book, tradeHistory] = await Promise.all([
        getOrderbook(ticker),
        getTrades(ticker),
      ]);
      setOrderbook(book);
      setTrades(tradeHistory);
      setStatusMessage("");
    } catch (error) {
      console.error(error);
      setStatusMessage("Unable to load market data for selected ticker.");
    } finally {
      setLoading(false);
    }
  };

  const fetchPortfolio = async (id) => {
    try {
      const data = await getPortfolio(id);
      setPortfolio(data);
      setStatusMessage("");
    } catch (error) {
      console.error(error);
      setPortfolio(null);
      setStatusMessage("Trader not found. Use a valid trader ID from the simulation.");
    }
  };

  useEffect(() => {
    fetchStocks();
    const interval = setInterval(fetchStocks, 3000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    fetchMarketData(selectedTicker);
    const interval = setInterval(() => fetchMarketData(selectedTicker), 3000);
    return () => clearInterval(interval);
  }, [selectedTicker]);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setStatusMessage("Submitting order...");

    try {
      await submitOrder(orderForm);
      setStatusMessage("Order submitted successfully.");
      fetchMarketData(orderForm.ticker);
      fetchStocks();
    } catch (error) {
      console.error(error);
      setStatusMessage("Order submission failed. Check console for details.");
    }
  };

  const bestBid = orderbook.bids[0];
  const bestAsk = orderbook.asks[0];

  return (
    <div className="app-shell">
      <header className="top-bar">
        <div>
          <h1>Market Simulator Dashboard</h1>
          <p>Live prices, order books, trades, and portfolio insights.</p>
        </div>
        <div className="status-chip">{statusMessage || "Connected"}</div>
      </header>

      <section className="layout-grid">
        <article className="panel panel-primary">
          <div className="panel-header">
            <h2>Live Stock Prices</h2>
            <span>{stocks.length} tickers</span>
          </div>
          <div className="table-scroll">
            <table>
              <thead>
                <tr>
                  <th>Ticker</th>
                  <th>Price</th>
                  <th>Volume</th>
                </tr>
              </thead>
              <tbody>
                {stocks.map((stock) => (
                  <tr
                    key={stock.ticker}
                    className={stock.ticker === selectedTicker ? "selected-row" : ""}
                    onClick={() => {
                      setSelectedTicker(stock.ticker);
                      setOrderForm((prev) => ({ ...prev, ticker: stock.ticker }));
                    }}
                  >
                    <td>{stock.ticker}</td>
                    <td>{formatCurrency(stock.price)}</td>
                    <td>{stock.volume}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </article>

        <article className="panel panel-secondary">
          <div className="panel-header">
            <h2>Submit Order</h2>
          </div>
          <form className="order-form" onSubmit={handleSubmit}>
            <label>
              Trader ID
              <input
                type="number"
                value={orderForm.trader_id}
                onChange={(event) =>
                  setOrderForm((prev) => ({
                    ...prev,
                    trader_id: Number(event.target.value),
                  }))
                }
                min="1"
              />
            </label>
            <label>
              Ticker
              <select
                value={orderForm.ticker}
                onChange={(event) => setOrderForm((prev) => ({ ...prev, ticker: event.target.value }))}
              >
                {stockOptions.map((ticker) => (
                  <option key={ticker} value={ticker}>
                    {ticker}
                  </option>
                ))}
              </select>
            </label>
            <label>
              Side
              <select
                value={orderForm.side}
                onChange={(event) => setOrderForm((prev) => ({ ...prev, side: event.target.value }))}
              >
                <option value="BUY">BUY</option>
                <option value="SELL">SELL</option>
              </select>
            </label>
            <label>
              Quantity
              <input
                type="number"
                value={orderForm.quantity}
                onChange={(event) =>
                  setOrderForm((prev) => ({ ...prev, quantity: Number(event.target.value) }))
                }
                min="1"
              />
            </label>
            <label>
              Price
              <input
                type="number"
                step="0.01"
                value={orderForm.price}
                onChange={(event) =>
                  setOrderForm((prev) => ({ ...prev, price: Number(event.target.value) }))
                }
                min="0"
              />
            </label>
            <button type="submit">Place Order</button>
          </form>
        </article>
      </section>

      <section className="layout-grid">
        <article className="panel">
          <div className="panel-header">
            <h2>Order Book</h2>
            <span>{selectedTicker}</span>
          </div>
          {loading ? (
            <div className="loading">Loading order book...</div>
          ) : (
            <div className="book-grid">
              <div>
                <h3>Asks</h3>
                <table>
                  <thead>
                    <tr>
                      <th>Price</th>
                      <th>Qty</th>
                      <th>Trader</th>
                    </tr>
                  </thead>
                  <tbody>
                    {orderbook.asks.map((order, index) => (
                      <tr key={`ask-${index}`}>
                        <td>{formatCurrency(order.price)}</td>
                        <td>{order.quantity}</td>
                        <td>{order.trader_id}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
              <div>
                <h3>Bids</h3>
                <table>
                  <thead>
                    <tr>
                      <th>Price</th>
                      <th>Qty</th>
                      <th>Trader</th>
                    </tr>
                  </thead>
                  <tbody>
                    {orderbook.bids.map((order, index) => (
                      <tr key={`bid-${index}`}>
                        <td>{formatCurrency(order.price)}</td>
                        <td>{order.quantity}</td>
                        <td>{order.trader_id}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </article>

        <article className="panel">
          <div className="panel-header">
            <h2>Trade History</h2>
            <span>{selectedTicker}</span>
          </div>
          <div className="table-scroll">
            <table>
              <thead>
                <tr>
                  <th>Price</th>
                  <th>Qty</th>
                  <th>Buyer</th>
                  <th>Seller</th>
                </tr>
              </thead>
              <tbody>
                {trades.slice(0, 20).map((trade, index) => (
                  <tr key={`trade-${index}`}>
                    <td>{formatCurrency(trade.price)}</td>
                    <td>{trade.quantity}</td>
                    <td>{trade.buyer}</td>
                    <td>{trade.seller}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </article>

        <article className="panel">
          <div className="panel-header">
            <h2>Portfolio Dashboard</h2>
          </div>
          <div className="panel-body">
            <label>
              Trader ID
              <input
                type="number"
                value={portfolioId}
                onChange={(event) => setPortfolioId(Number(event.target.value))}
                min="1"
              />
            </label>
            <button onClick={() => fetchPortfolio(portfolioId)}>Load Portfolio</button>
            {portfolio ? (
              <div className="portfolio-details">
                <p>
                  <strong>Cash:</strong> {formatCurrency(portfolio.cash)}
                </p>
                <div className="positions-list">
                  <h3>Positions</h3>
                  {Object.keys(portfolio.positions).length ? (
                    <ul>
                      {Object.entries(portfolio.positions).map(([symbol, qty]) => (
                        <li key={symbol}>
                          {symbol}: {qty}
                        </li>
                      ))}
                    </ul>
                  ) : (
                    <p>No positions found.</p>
                  )}
                </div>
              </div>
            ) : (
              <p className="hint">Load a trader portfolio to view positions and cash.</p>
            )}
          </div>
        </article>

        <article className="panel panel-stats">
          <div className="panel-header">
            <h2>Market Statistics</h2>
          </div>
          <div className="stats-grid">
            <div className="stat-card">
              <span className="stat-value">{stocks.length}</span>
              <span className="stat-label">Tracked tickers</span>
            </div>
            <div className="stat-card">
              <span className="stat-value">{bestBid ? formatCurrency(bestBid.price) : "—"}</span>
              <span className="stat-label">Best bid ({selectedTicker})</span>
            </div>
            <div className="stat-card">
              <span className="stat-value">{bestAsk ? formatCurrency(bestAsk.price) : "—"}</span>
              <span className="stat-label">Best ask ({selectedTicker})</span>
            </div>
            <div className="stat-card">
              <span className="stat-value">{trades.length}</span>
              <span className="stat-label">Recent trades</span>
            </div>
          </div>
        </article>
      </section>
    </div>
  );
}
