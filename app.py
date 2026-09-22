import os
import requests
from dotenv import load_dotenv

load_dotenv()

NANSEN_API_KEY = os.getenv("NANSEN_API_KEY")

if not NANSEN_API_KEY:
    raise ValueError("Nansen API key not found.")

url = "https://api.nansen.ai/api/v1/prediction-market/market-screener"

headers = {
    "apiKey": NANSEN_API_KEY,
    "Content-Type": "application/json"
}

payload = {
    "order_by": [
        {
            "direction": "DESC",
            "field": "volume_24hr"
        }
    ],
    "query": "NFL",
    "status": "active"
}

print("\n🐾 FUTBOL FRENCHIE PREDICTS")
print("=" * 60)
print("Scanning Nansen for active NFL prediction markets...\n")

response = requests.post(url, headers=headers, json=payload, timeout=30)

if not response.ok:
    print("❌ Nansen request failed:", response.status_code)
    print(response.text)
    raise SystemExit

data = response.json()
markets = data.get("data", [])

print(f"✅ Found {len(markets)} NFL markets\n")

for number, market in enumerate(markets, start=1):
    print(f"{number}. {market.get('question', 'Unknown Market')}")
    print(f"   Market ID: {market.get('market_id', 'N/A')}")
    print(f"   Last Price: {market.get('last_trade_price', 'N/A')}")
    print(f"   Best Bid: {market.get('best_bid', 'N/A')}")
    print(f"   Best Ask: {market.get('best_ask', 'N/A')}")
    print(f"   24H Volume: ${market.get('volume_24hr', 0):,.2f}")
    print(f"   Liquidity: ${market.get('liquidity', 0):,.2f}")
    print(f"   Open Interest: ${market.get('open_interest', 0):,.2f}")
    print(f"   24H Traders: {market.get('unique_traders_24h', 0)}")
    print("-" * 60)

while True:
    choice = input("\nEnter the number of the market you want to analyze: ")

    try:
        choice = int(choice)

        if 1 <= choice <= len(markets):
            selected_market = markets[choice - 1]
            break

        print("Please choose a number from the list.")

    except ValueError:
        print("Please enter a number.")

print("\n🐾 SELECTED MARKET")
print("=" * 60)
print(selected_market.get("question"))
print("Market ID:", selected_market.get("market_id"))
print("=" * 60)
print("Ready for deeper Nansen analysis.")

market_id = str(selected_market.get("market_id"))

ohlcv_url = "https://api.nansen.ai/api/v1/prediction-market/ohlcv"

ohlcv_payload = {
    "market_id": market_id,
    "pagination": {
        "page": 1,
        "per_page": 10
    },
    "order_by": [
        {
            "direction": "DESC",
            "field": "period_start"
        }
    ]
}

print("\nLoading Nansen price history...")

ohlcv_response = requests.post(
    ohlcv_url,
    headers=headers,
    json=ohlcv_payload,
    timeout=30
)

print("OHLCV status:", ohlcv_response.status_code)

market_id = str(selected_market.get("market_id"))

def nansen_post(endpoint, payload):
    url = f"https://api.nansen.ai/api/v1/prediction-market/{endpoint}"
    response = requests.post(url, headers=headers, json=payload, timeout=30)

    if not response.ok:
        print(f"❌ {endpoint} failed: {response.status_code}")
        return None

    return response.json()

print("\n🔎 Starting deeper Nansen analysis...")

# Analyze Nansen OHLCV price history
if ohlcv_response.ok:
    ohlcv_data = ohlcv_response.json()
    candles = ohlcv_data.get("data", [])

    if candles:
        yes_candles = [c for c in candles if c.get("side") == "Yes"]

        if yes_candles:
            yes_candles.sort(key=lambda x: x.get("period_start", ""))

            first = yes_candles[0]
            latest = yes_candles[-1]

            first_price = float(first.get("close", 0) or 0)
            latest_price = float(latest.get("close", 0) or 0)

            total_volume = sum(float(c.get("volume_usd", 0) or 0) for c in yes_candles)
            total_trades = sum(int(c.get("trade_count", 0) or 0) for c in yes_candles)

            if first_price > 0:
                price_change_pct = ((latest_price - first_price) / first_price) * 100
            else:
                price_change_pct = 0

            print("\n📈 NANSEN PRICE ANALYSIS")
            print("=" * 60)
            print(f"YES Price: {latest_price:.3f}")
            print(f"Implied Probability: {latest_price * 100:.1f}%")
            print(f"Period Start Price: {first_price:.3f}")
            print(f"Price Change: {price_change_pct:+.1f}%")
            print(f"Analyzed Volume: ${total_volume:,.2f}")
            print(f"Analyzed Trades: {total_trades}")
            print("=" * 60)
        else:
            print("No YES-side OHLCV candles returned by Nansen.")
    else:
        print("No OHLCV price-history data returned by Nansen.")

# Get Nansen orderbook data
print("\n💧 Loading Nansen orderbook and liquidity data...")

orderbook_data = nansen_post(
    "orderbook",
    {
        "market_id": market_id,
        "pagination": {
            "page": 1,
            "per_page": 50
        }
    }
)

if orderbook_data:
    orders = orderbook_data.get("data", [])

    if orders:
        buy_orders = [o for o in orders if o.get("side") == "buy"]
        sell_orders = [o for o in orders if o.get("side") == "sell"]

        total_buy_size = sum(float(o.get("size", 0) or 0) for o in buy_orders)
        total_sell_size = sum(float(o.get("size", 0) or 0) for o in sell_orders)

        print("\n💧 NANSEN ORDERBOOK ANALYSIS")
        print("=" * 60)
        print(f"Orders Analyzed: {len(orders)}")
        print(f"Buy Orders: {len(buy_orders)}")
        print(f"Sell Orders: {len(sell_orders)}")
        print(f"Buy-Side Size: {total_buy_size:,.2f}")
        print(f"Sell-Side Size: {total_sell_size:,.2f}")
        print("=" * 60)
    else:
        print("No orderbook data returned by Nansen.")

# Get Nansen top-holder data
print("\n🐋 Loading Nansen top holders...")


holders = []

top_holders_data = nansen_post(
    "top-holders",
    {
        "market_id": market_id,
        "pagination": {
            "page": 1,
            "per_page": 10
        },
        "order_by": [
            {
                "direction": "DESC",
                "field": "position_size"
            }
        ]
    }
)

if top_holders_data:
    holders = top_holders_data.get("data", [])

    if holders:
        print("\n🐋 NANSEN TOP HOLDERS")
        print("=" * 60)

        for i, holder in enumerate(holders[:5], 1):
            address = holder.get("address", "Unknown")
            side = holder.get("side", "Unknown")
            position_size = float(holder.get("position_size", 0) or 0)
            avg_entry = float(holder.get("avg_entry_price", 0) or 0)
            current_price = float(holder.get("current_price", 0) or 0)
            unrealized_pnl = float(holder.get("unrealized_pnl_usd", 0) or 0)

            short_address = (
                f"{address[:6]}...{address[-4:]}"
                if len(address) > 12
                else address
            )

            print(f"#{i} {short_address}")
            print(f"   Side: {side}")
            print(f"   Position Size: {position_size:,.2f}")
            print(f"   Avg Entry: {avg_entry:.4f}")
            print(f"   Current Price: {current_price:.4f}")
            print(f"   Unrealized PnL: ${unrealized_pnl:,.2f}")

        print("=" * 60)
    else:
        print("No top-holder data returned by Nansen.")



# Wallet concentration risk
if holders:
    top_positions = [
        float(holder.get("position_size", 0) or 0)
        for holder in holders
    ]

    total_top_positions = sum(top_positions)
    largest_position = max(top_positions) if top_positions else 0

    if total_top_positions > 0:
        largest_holder_share = (
            largest_position / total_top_positions
        ) * 100
    else:
        largest_holder_share = 0

    print("\n⚠️ WALLET CONCENTRATION CHECK")
    print("=" * 60)
    print(
        f"Largest holder share of sampled top-holder positions: "
        f"{largest_holder_share:.1f}%"
    )

    if largest_holder_share >= 50:
        concentration_risk = "HIGH"
        print("Concentration Risk: HIGH")
        print(
            "One wallet represents a very large share of the "
            "sampled top-holder positioning."
        )
    elif largest_holder_share >= 30:
        concentration_risk = "ELEVATED"
        print("Concentration Risk: ELEVATED")
        print(
            "A single wallet represents a significant share of "
            "the sampled top-holder positioning."
        )
    else:
        concentration_risk = "LOW"
        print("Concentration Risk: LOW")
        print(
            "No single wallet dominates the sampled top-holder "
            "positioning."
        )

    print(
        "Note: concentration can increase market sensitivity to "
        "large-wallet activity; it does not prove manipulation."
    )
    print("=" * 60)# Get Nansen market trade flow
print("\n🔄 Loading Nansen market trade flow...")

trades_data = nansen_post(
    "trades-by-market",
    {
        "market_id": market_id,
        "pagination": {
            "page": 1,
            "per_page": 50
        },
        "order_by": [
            {
                "direction": "DESC",
                "field": "timestamp"
            }
        ]
    }
)

if trades_data:
    trades = trades_data.get("data", [])

    if trades:
        # Group multiple fills from the same transaction together
        transactions = {}

        for trade in trades:
            tx_hash = trade.get("tx_hash") or f"unknown-{len(transactions)}"

            if tx_hash not in transactions:
                transactions[tx_hash] = {
                    "action": trade.get("taker_action", "Unknown"),
                    "side": trade.get("side", "Unknown"),
                    "size": 0.0,
                    "value": 0.0
                }

            transactions[tx_hash]["size"] += float(trade.get("size", 0) or 0)
            transactions[tx_hash]["value"] += float(trade.get("usdc_value", 0) or 0)

        unique_trades = list(transactions.values())

        buy_value = sum(
            t["value"] for t in unique_trades
            if str(t["action"]).lower() == "buy"
        )

        sell_value = sum(
            t["value"] for t in unique_trades
            if str(t["action"]).lower() == "sell"
        )

        print("\n🔄 NANSEN TRADE FLOW")
        print("=" * 60)
        print(f"Fills Analyzed: {len(trades)}")
        print(f"Unique Transactions: {len(unique_trades)}")
        print(f"Buy Flow: ${buy_value:,.2f}")
        print(f"Sell Flow: ${sell_value:,.2f}")
        print(f"Net Taker Flow: ${buy_value - sell_value:+,.2f}")
        print("=" * 60)
    else:
        print("No recent market trades returned by Nansen.")

# Get Nansen PnL leaders for this market
print("\n🏆 Loading Nansen market PnL leaders...")

pnl_market_data = nansen_post(
    "pnl-by-market",
    {
        "market_id": market_id,
        "pagination": {
            "page": 1,
            "per_page": 10
        },
        "order_by": [
            {
                "direction": "DESC",
                "field": "total_pnl_usd"
            }
        ]
    }
)

if pnl_market_data:
    pnl_leaders = pnl_market_data.get("data", [])

    if pnl_leaders:
        print("\n🏆 NANSEN MARKET PNL LEADERS")
        print("=" * 60)

        for i, trader in enumerate(pnl_leaders[:5], 1):
            address = trader.get("address", "Unknown")
            side_held = trader.get("side_held") or "None"

            total_pnl = float(trader.get("total_pnl_usd", 0) or 0)
            unrealized_value = float(
                trader.get("unrealized_value_usd", 0) or 0
            )
            sell_proceeds = float(
                trader.get("net_sell_proceeds_usd", 0) or 0
            )
            redemption_value = float(
                trader.get("redemption_value_usd", 0) or 0
            )

            short_address = (
                f"{address[:6]}...{address[-4:]}"
                if len(address) > 12
                else address
            )

            print(f"#{i} {short_address}")
            print(f"   Side Held: {side_held}")
            print(f"   Nansen Total PnL: ${total_pnl:,.2f}")
            print(f"   Unrealized Value: ${unrealized_value:,.2f}")
            print(f"   Net Sell Proceeds: ${sell_proceeds:,.2f}")
            print(f"   Redemption Value: ${redemption_value:,.2f}")

        print("=" * 60)
    else:
        print("No market PnL data returned by Nansen.")

# Futbol Frenchie Predicts - Nansen Signal Engine
print("\n🐾 FUTBOL FRENCHIE PREDICTS")
print("=" * 60)
print(selected_market.get("question", "Selected Market"))
print(f"Market ID: {market_id}")
print("-" * 60)

signals = []
signal_score = 0

# Price momentum
if "price_change_pct" in locals():
    if price_change_pct >= 5:
        signals.append(
            f"📈 YES momentum is positive ({price_change_pct:+.1f}%)."
        )
        signal_score += 1
    elif price_change_pct <= -5:
        signals.append(
            f"📉 YES momentum is negative ({price_change_pct:+.1f}%)."
        )
        signal_score -= 1
    else:
        signals.append(
            f"➡️ YES price is relatively stable ({price_change_pct:+.1f}%)."
        )

# Recent taker trade flow
if "buy_value" in locals() and "sell_value" in locals():
    net_flow = buy_value - sell_value

    if net_flow > 0:
        signals.append(
            f"🟢 Recent taker flow favors buys by ${net_flow:,.2f}."
        )
        signal_score += 1
    elif net_flow < 0:
        signals.append(
            f"🔴 Recent taker flow favors sells by ${abs(net_flow):,.2f}."
        )
        signal_score -= 1
    else:
        signals.append("⚪ Recent taker buy/sell flow is balanced.")

# Top-holder positioning
if "holders" in locals() and holders:
    yes_holders = sum(
        1 for holder in holders[:5]
        if str(holder.get("side", "")).lower() == "yes"
    )

    signals.append(
        f"🐋 {yes_holders} of the top 5 displayed holders are positioned YES."
    )

# Display current market probability
if "latest_price" in locals():
    signals.insert(
        0,
        f"🎯 Current YES implied probability: {latest_price * 100:.1f}%."
    )

print("\nNANSEN EVIDENCE")
for signal in signals:
    print(signal)

print("\nRESEARCH READ")

if signal_score >= 2:
    print("🟢 Recent Nansen market signals are strengthening for YES.")
elif signal_score <= -2:
    print("🔴 Recent Nansen market signals are weakening for YES.")
else:
    print("🟡 Nansen signals are mixed. No strong directional read yet.")

print(
    "This is market-research context, not a prediction of the NFL outcome."
)
print("=" * 60)

# Futbol Frenchie Predicts - Entry / Exit Research
print("\n🎯 ENTRY / EXIT RESEARCH")
print("=" * 60)

entry_notes = []
risk_notes = []

# Current market price context
if "latest_price" in locals():
    entry_notes.append(
        f"Current YES market price: {latest_price:.3f} "
        f"({latest_price * 100:.1f}% implied probability)."
    )

# Momentum context
if "price_change_pct" in locals():
    if price_change_pct <= -5:
        entry_notes.append(
            "YES is trading with negative recent price momentum."
        )
    elif price_change_pct >= 5:
        entry_notes.append(
            "YES is trading with positive recent price momentum."
        )
    else:
        entry_notes.append(
            "YES has not shown a major recent directional price move."
        )

# Trade-flow context
if "buy_value" in locals() and "sell_value" in locals():
    net_flow = buy_value - sell_value

    if net_flow < 0:
        entry_notes.append(
            "Recent taker flow is sell-heavy; waiting for buy flow "
            "to improve could provide stronger confirmation."
        )
    elif net_flow > 0:
        entry_notes.append(
            "Recent taker flow is buy-heavy, providing some "
            "confirmation of current demand."
        )
    else:
        entry_notes.append(
            "Recent taker flow is balanced."
        )

# Holder context
if "holders" in locals() and holders:
    yes_holders = sum(
        1 for holder in holders[:5]
        if str(holder.get("side", "")).lower() == "yes"
    )

    if yes_holders >= 4:
        entry_notes.append(
            "Large displayed holders show strong YES positioning, "
            "but holder size alone does not establish trader skill."
        )

# Liquidity / orderbook warning
if "sell_orders" in locals() and len(sell_orders) == 0:
    risk_notes.append(
        "Only buy orders appeared in the sampled orderbook page, "
        "so this sample cannot establish full two-sided depth."
    )

print("\nENTRY CONTEXT")
for note in entry_notes:
    print(f"• {note}")

print("\nEXIT / RISK WATCH")
print("• Watch for a reversal in price momentum.")
print("• Watch for taker flow to shift direction.")
print("• Re-check liquidity before sizing an entry or exit.")

for note in risk_notes:
    print(f"• {note}")

print("\nCURRENT SETUP")

if signal_score <= -2:
    print(
        "⏳ WAIT / WATCH — current Nansen evidence does not yet "
        "show strong YES confirmation."
    )
elif signal_score >= 2:
    print(
        "👀 CONFIRMATION BUILDING — Nansen market evidence is "
        "strengthening, but price and liquidity still matter."
    )
else:
    print(
        "⚖️ MIXED — wait for clearer agreement between momentum "
        "and trade flow."
    )

print("=" * 60)

# Futbol Frenchie Predicts - Trader Quality Validation
print("\n🧠 TRADER QUALITY CHECK")
print("=" * 60)

holder_addresses = set()

if "holders" in locals() and holders:
    for holder in holders[:5]:
        address = str(holder.get("address", "")).lower()
        if address:
            holder_addresses.add(address)

profitable_market_traders = []
matched_profitable_holders = []

if "pnl_leaders" in locals() and pnl_leaders:
    for trader in pnl_leaders:
        address = str(trader.get("address", "")).lower()
        total_pnl = float(trader.get("total_pnl_usd", 0) or 0)

        if total_pnl > 0:
            profitable_market_traders.append(
                {
                    "address": address,
                    "pnl": total_pnl
                }
            )

            if address in holder_addresses:
                matched_profitable_holders.append(
                    {
                        "address": address,
                        "pnl": total_pnl
                    }
                )

print(
    f"Positive-PnL traders in Nansen sample: "
    f"{len(profitable_market_traders)}"
)

print(
    f"Top holders also appearing as positive-PnL traders: "
    f"{len(matched_profitable_holders)}"
)

if matched_profitable_holders:
    print(
        "🟢 Some large holders overlap with positive-PnL addresses "
        "in Nansen's market data."
    )
else:
    print(
        "⚪ No positive-PnL overlap was verified between the displayed "
        "top holders and this PnL sample."
    )

print(
    "Trader-quality evidence is treated separately from position size."
)
print("=" * 60)

# Futbol Frenchie Predicts - Final Research Report
print("\n" + "=" * 60)
print("🐾 FUTBOL FRENCHIE PREDICTS — FINAL REPORT")
print("=" * 60)

print(f"\nMARKET")
print(selected_market.get("question", "Selected Market"))
print(f"Market ID: {market_id}")

if "latest_price" in locals():
    print(
        f"\nYES PRICE: {latest_price:.3f} "
        f"({latest_price * 100:.1f}% implied probability)"
    )

print("\nMARKET SIGNALS")

if "price_change_pct" in locals():
    print(f"• Price Momentum: {price_change_pct:+.1f}%")

if "buy_value" in locals() and "sell_value" in locals():
    final_net_flow = buy_value - sell_value
    print(f"• Net Taker Flow: ${final_net_flow:+,.2f}")

if "holders" in locals() and holders:
    final_yes_holders = sum(
        1 for holder in holders[:5]
        if str(holder.get("side", "")).lower() == "yes"
    )
    print(
        f"• Top Holder Positioning: "
        f"{final_yes_holders}/5 displayed holders on YES"
    )

if "matched_profitable_holders" in locals():
    print(
        f"• Positive-PnL Holder Overlap: "
        f"{len(matched_profitable_holders)}"
    )
if "concentration_risk" in locals():
    print(
        f"• Wallet Concentration Risk: {concentration_risk} "
        f"({largest_holder_share:.1f}% largest sampled holder)"
    )

print("\nSETUP")

if signal_score <= -2:
    final_setup = "WAIT / WATCH"
    final_reason = (
        "Momentum and recent trade flow do not yet provide "
        "strong YES confirmation."
    )
elif signal_score >= 2:
    final_setup = "CONFIRMATION BUILDING"
    final_reason = (
        "Multiple Nansen market signals are strengthening, "
        "but entry price and liquidity still require review."
    )
else:
    final_setup = "MIXED"
    final_reason = (
        "Nansen signals are not aligned strongly enough "
        "for a clear directional market read."
    )

print(f"• Research Setup: {final_setup}")
print(f"• Why: {final_reason}")

print("\nWHAT TO WATCH NEXT")

if "price_change_pct" in locals() and price_change_pct < 0:
    print("• Watch for YES price momentum to stabilize or reverse.")

if "buy_value" in locals() and "sell_value" in locals():
    if buy_value < sell_value:
        print("• Watch for taker buy flow to begin exceeding sell flow.")
    else:
        print("• Watch whether positive taker flow persists.")

if "matched_profitable_holders" in locals():
    if len(matched_profitable_holders) > 0:
        print(
            "• Monitor whether validated holder activity continues "
            "or begins reducing exposure."
        )
    else:
        print(
            "• Look for stronger trader-quality confirmation "
            "before treating whale positioning as meaningful."
        )

print("• Re-check orderbook depth before sizing any position.")

print("\nNANSEN DATA USED")
print(
    "Market Screener • OHLCV • Orderbook • Top Holders • "
    "Trades by Market • PnL by Market"
)

print(
    "\nResearch tool only — this report describes prediction-market "
    "activity and does not predict the NFL result."
)
print("=" * 60)

# Final demo summary
print("\n" + "=" * 60)
print("🐾 FUTBOL FRENCHIE PREDICTS — NANSEN NFL MARKET REPORT")
print("=" * 60)

print(f"Market: {selected_market.get('question', 'Unknown market')}")
print(f"Market ID: {market_id}")

if "latest_price" in locals():
    print(f"YES Probability: {latest_price * 100:.1f}%")

if "price_change_pct" in locals():
    print(f"Recent Price Momentum: {price_change_pct:+.1f}%")

if "net_flow" in locals():
    print(f"Recent Net Taker Flow: ${net_flow:,.2f}")

if "yes_holders" in locals():
    print(f"Top Holder YES Positioning: {yes_holders}/5")

if "matched_profitable_holders" in locals():
    print(
        f"Positive-PnL Holder Overlap: "
        f"{len(matched_profitable_holders)}"
    )

if "signal_score" in locals():
    if signal_score >= 2:
        setup = "CONFIRMATION BUILDING"
    elif signal_score <= -2:
        setup = "WAIT / WATCH"
    else:
        setup = "MIXED"

    print(f"Current Research Setup: {setup}")

print("\nPowered by Nansen Prediction Market data.")
print("Research context only — not a prediction of the NFL outcome.")
print("=" * 60)