# 🐾 Futbol Frenchie Predicts

**NFL prediction-market research powered by Nansen data.**

Futbol Frenchie Predicts is a research tool that analyzes NFL prediction markets using Nansen's Prediction Market API. Instead of looking at price alone, it combines market momentum, liquidity, trade flow, holder positioning, and trader performance into one research report.

## 🔍 What It Analyzes

- NFL prediction-market discovery
- YES price / implied probability
- Recent price momentum
- Trading volume and activity
- Orderbook liquidity
- Buy vs. sell taker flow
- Top-holder positioning
- Trader performance and PnL
- Positive-PnL trader overlap
- Entry / exit research context
- Overall market setup: **CONFIRMATION BUILDING**, **MIXED**, or **WAIT / WATCH**

## 🧠 Research Pipeline

Market Screener  
↓  
OHLCV / Price History  
↓  
Orderbook & Liquidity  
↓  
Top Holders  
↓  
Trades by Market  
↓  
Trader Performance / PnL  
↓  
Signal Engine  
↓  
NFL Prediction-Market Research Report

## 📊 Nansen Data Used

The project uses Nansen Prediction Market endpoints including:

- Market Screener
- OHLCV
- Orderbook
- Top Holders
- Trades by Market
- Trades by Address
- PnL by Market
- PnL by Address

## 🏈 Example Output

The final report can surface information such as:

- Current YES implied probability
- Recent price momentum
- Recent net taker flow
- Top-holder YES positioning
- Positive-PnL holder overlap
- Current research setup
- Conditions worth monitoring next

This allows a user to move from **“I like this NFL outcome”** to **“What is the prediction market actually showing me right now?”**

## 🔐 Setup

Create a local `.env` file:

```text
NANSEN_API_KEY=your_nansen_api_key
