from langchain.tools import Tool
from langchain_community.utilities.alpha_vantage import AlphaVantageAPIWrapper
import matplotlib.pyplot as plt
import pandas as pd
import io
import base64
from PIL import Image

# Initialize Alpha Vantage API
alpha_vantage = AlphaVantageAPIWrapper()

# Custom function to wrap multiple Alpha Vantage endpoints
def get_financial_data(query: str) -> str:
    try:
        query = query.strip().lower()
        if "exchange rate" in query or "convert" in query:
            # Example: "Get exchange rate USD to JPY"
            parts = query.split()
            from_currency = parts[-3].upper()
            to_currency = parts[-1].upper()
            result = alpha_vantage._get_exchange_rate(from_currency, to_currency)
            return str(result)
        
        elif "daily stock" in query:
            # Example: "Get daily stock for IBM"
            symbol = query.split()[-1].upper()
            result = alpha_vantage._get_time_series_daily(symbol)
            return str(result)
        
        elif "weekly stock" in query:
            # Example: "Get weekly stock for IBM"
            symbol = query.split()[-1].upper()
            result = alpha_vantage._get_time_series_weekly(symbol)
            return str(result)

        elif "stock quote" in query or "price of" in query:
            # Example: "Get stock quote for IBM"
            symbol = query.split()[-1].upper()
            result = alpha_vantage._get_quote_endpoint(symbol)
            return str(result)
        
        elif "search symbol" in query:
            # Example: "Search symbol IB"
            symbol = query.split()[-1].upper()
            result = alpha_vantage.search_symbols(symbol)
            return str(result)

        elif "market news" in query:
            # Example: "Get market news for IBM"
            symbol = query.split()[-1].upper()
            result = alpha_vantage._get_market_news_sentiment(symbol)
            return str(result)

        elif "top gainers" in query or "top losers" in query:
            result = alpha_vantage._get_top_gainers_losers()
            return str(result)

        else:
            return "Unsupported query. Try: exchange rate, daily stock, weekly stock, quote, market news, etc."
    
    except Exception as e:
        return f"Error: {str(e)}"

def generate_financial_chart(query: str) -> str:
    try:
        query = query.strip().lower()
        if "daily chart" in query:
            symbol = query.split()[-1].upper()
            data = alpha_vantage._get_time_series_daily(symbol)

            timeseries = data["Time Series (Daily)"]
            df = pd.DataFrame(timeseries).T
            df.index = pd.to_datetime(df.index)
            df = df.sort_index()
            df = df.astype(float)

            plt.figure(figsize=(10, 5))
            plt.plot(df.index, df["4. close"], label=f"{symbol} Closing Price", color="blue")
            plt.title(f"{symbol} - Daily Closing Prices")
            plt.xlabel("Date")
            plt.ylabel("Price (USD)")
            plt.grid(True)
            plt.legend()

        elif "volume chart" in query:
            symbol = query.split()[-1].upper()
            data = alpha_vantage._get_time_series_daily(symbol)

            timeseries = data["Time Series (Daily)"]
            df = pd.DataFrame(timeseries).T
            df.index = pd.to_datetime(df.index)
            df = df.sort_index()
            df = df.astype(float)

            plt.figure(figsize=(10, 5))
            plt.bar(df.index, df["5. volume"], color="green")
            plt.title(f"{symbol} - Daily Volume")
            plt.xlabel("Date")
            plt.ylabel("Volume")
            plt.grid(True)

        else:
            return "Please use a query like 'daily chart for AAPL' or 'volume chart for IBM'."

        # Save plot to buffer
        buf = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format="png")
        plt.close()
        buf.seek(0)

        # Use PIL to open the image and save it to disk
        img = Image.open(buf)
        filename = f"{symbol}_chart.png"
        img.save(filename)

        return f"Chart saved as file: {filename}"

    except Exception as e:
        return f"Chart generation failed: {str(e)}"