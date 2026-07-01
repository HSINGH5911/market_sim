const BASE_URL = "http://127.0.0.1:8000";

const jsonHeaders = {
  "Content-Type": "application/json",
};

const handleResponse = async (response) => {
  if (!response.ok) {
    const body = await response.json().catch(() => null);
    const message = body?.detail || body?.message || response.statusText;
    throw new Error(message || "Network error");
  }
  return response.json();
};

export const getStocks = () =>
  fetch(`${BASE_URL}/stocks`).then(handleResponse);

export const getOrderbook = (ticker) =>
  fetch(`${BASE_URL}/orderbook/${ticker}`).then(handleResponse);

export const getTrades = (ticker) =>
  fetch(`${BASE_URL}/trades/${ticker}`).then(handleResponse);

export const getPortfolio = (traderId) =>
  fetch(`${BASE_URL}/portfolio/${traderId}`).then(handleResponse);

export const submitOrder = (order) =>
  fetch(`${BASE_URL}/order`, {
    method: "POST",
    headers: jsonHeaders,
    body: JSON.stringify(order),
  }).then(handleResponse);
