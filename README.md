# Market Simulator

This repository contains a market simulation backend and a React frontend dashboard.

## Backend

Run the backend simulation and API server:

```bash
python app.py
```

This starts the simulation and exposes FastAPI endpoints on `http://127.0.0.1:8000`.

## Frontend

From the `frontend` directory, install dependencies and start the React app:

```bash
cd frontend
npm install
npm run dev
```

Then open the browser at `http://127.0.0.1:5173`.

## Available frontend features

- Live stock prices
- Order book view
- Trade history view
- Portfolio dashboard
- Market statistics dashboard
