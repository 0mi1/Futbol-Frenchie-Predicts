# 🐾 Futbol Frenchie Predicts

NFL prediction-market research powered by the Nansen Prediction Market API.

The app scans active NFL markets, lets a user choose one, and turns live market data into a research report. It compares price momentum and recent trade flow, checks orderbook liquidity and holder concentration, and looks for overlap between large holders and traders with positive market PnL. The final setup is **CONFIRMATION BUILDING**, **MIXED**, or **WAIT / WATCH**. It describes market evidence; it does not predict game results or place trades.

## What the app uses

The running app calls these Nansen Prediction Market endpoints:

1. Market Screener — discover active NFL markets.
2. OHLCV — inspect recent YES price history and implied probability.
3. Orderbook — inspect sampled buy and sell depth.
4. Top Holders — inspect displayed holder positioning and concentration.
5. Trades by Market — summarize recent taker buy and sell flow.
6. PnL by Market — compare sampled profitable traders with large holders.

These inputs feed the signal engine, entry and exit research notes, and final market report. A positive market signal is not a claim that the NFL outcome is more likely than its market price suggests.

## Run locally

Requirements: Python 3 and a Nansen API key with access to the Prediction Market endpoints.

```bash
git clone https://github.com/0mi1/Futbol-Frenchie-Predicts.git
cd Futbol-Frenchie-Predicts
python3 -m venv .venv
source .venv/bin/activate
pip install requests python-dotenv
```

Create a `.env` file in the project folder containing:

```text
NANSEN_API_KEY=your_nansen_api_key
```

Then run:

```bash
python app.py
```

The app prints numbered active NFL markets. Enter one number and press Return. It fetches live Nansen data and prints its analysis and final report in Terminal. Each run uses API credits. If no active markets are returned, try again when Nansen has active NFL markets; the current version expects at least one result.

## Example research interpretation

A market can have positive YES price momentum while recent taker flow is negative. In that case the app can return **MIXED**, explain the conflict, and flag liquidity or holder concentration for review. The report is research context, not betting or financial advice.

## Security

Keep `.env` local and never commit an API key. The repository's `.gitignore` should exclude `.env` and `.venv`.

## Built for the Nansen Meridian Buildathon

The 30–60 second demo shows the app using live Nansen data and producing its final report. The public repository contains the code and setup instructions so another builder can run it.
