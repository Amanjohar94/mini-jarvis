# modules/markets.py

import yfinance as yf

def get_stock_data(symbol="AAPL"):
    try:
        data = yf.download(symbol, period="5d", interval="1h")
        return data["Close"]
    except Exception as e:
        print("Market fetch error:", e)
        return {}
