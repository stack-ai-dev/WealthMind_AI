import yfinance as yf
import requests
from typing import Optional


# Tickers we always fetch as a market overview
MARKET_TICKERS = {
    "S&P 500": "^GSPC",
    "Nasdaq": "^IXIC",
    "Gold": "GLD",
    "US Bonds (AGG)": "AGG",
}

CRYPTO_IDS = ["bitcoin", "ethereum"]   # CoinGecko IDs


def get_stock_data(ticker: str) -> Optional[dict]:
    """
    Fetches basic info for a single stock/ETF ticker.
    Returns None if fetch fails (network error, bad ticker, etc.)
    """
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="5d")   # last 5 trading days

        if hist.empty:
            return None

        latest_price = hist["Close"].iloc[-1]
        prev_price = hist["Close"].iloc[-2] if len(hist) > 1 else latest_price
        change_pct = ((latest_price - prev_price) / prev_price) * 100

        return {
            "ticker": ticker,
            "price": round(latest_price, 2),
            "change_percent": round(change_pct, 2),
            "trend": "up" if change_pct > 0 else "down",
        }
    except Exception as e:
        print(f"[WARN] Could not fetch {ticker}: {e}")
        return None


def get_crypto_prices() -> dict:
    """
    Fetches current Bitcoin and Ethereum prices from CoinGecko (free, no API key).
    Returns empty dict if API is unreachable.
    """
    try:
        ids = ",".join(CRYPTO_IDS)
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=usd&include_24hr_change=true"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()

        result = {}
        for coin_id in CRYPTO_IDS:
            if coin_id in data:
                result[coin_id] = {
                    "price_usd": data[coin_id].get("usd", 0),
                    "change_24h": round(data[coin_id].get("usd_24h_change", 0), 2),
                }
        return result

    except Exception as e:
        print(f"[WARN] Could not fetch crypto prices: {e}")
        return {}


def get_market_summary() -> str:
    """
    Creates a human-readable market summary string.
    This gets passed to the LLM for context-aware advice.
    
    Example output:
    "S&P 500 is at 5420.1 (+0.5%). Bitcoin is at $67,000 (+2.1% 24h)."
    """
    parts = []

    # Fetch stock indices
    for name, ticker in MARKET_TICKERS.items():
        data = get_stock_data(ticker)
        if data:
            direction = "+" if data["change_percent"] >= 0 else ""
            parts.append(f"{name}: {data['price']} ({direction}{data['change_percent']}%)")

    # Fetch crypto
    crypto = get_crypto_prices()
    if "bitcoin" in crypto:
        btc = crypto["bitcoin"]
        parts.append(f"Bitcoin: ${btc['price_usd']:,} ({btc['change_24h']:+.1f}% 24h)")
    if "ethereum" in crypto:
        eth = crypto["ethereum"]
        parts.append(f"Ethereum: ${eth['price_usd']:,} ({eth['change_24h']:+.1f}% 24h)")

    if not parts:
        return "Market data temporarily unavailable."

    return " | ".join(parts)
