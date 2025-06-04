import pandas as pd
import yfinance as yf
import httpx
from datetime import datetime

class FinancialAnalyzer:
    def __init__(self):
        self.treasury_api = "https://home.treasury.gov/resource-center/data-chart-center/interest-rates/daily-treasury-rates.csv"

    async def fetch_treasury_data(self):
        """
        Downloads the latest Treasury data CSV from the Treasury website.
        """
        url = "https://www.treasury.gov/resource-center/data-chart-center/interest-rates/Datasets/yield.xml"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
        df = pd.read_xml(response.text)
        df["Date"] = pd.to_datetime(df["Date"])
        df = df.set_index("Date")
        df = df.sort_index()
        return df

    def calculate_yield_spread(self, df: pd.DataFrame, long='10 Yr', short='2 Yr'):
        """
        Calculate the yield spread between two maturities.
        """
        df['Yield_Spread'] = df[long] - df[short]
        return df[['Yield_Spread']]

    def fetch_stock_data(self, ticker="^GSPC", period="1y", interval="1d"):
        """
        Fetch stock data using yfinance.
        """
        data = yf.download(ticker, period=period, interval=interval)
        return data

    def add_sma(self, df: pd.DataFrame, window=50):
        df[f"SMA_{window}"] = df['Close'].rolling(window=window).mean()
        return df

    def add_volatility(self, df: pd.DataFrame, window=20):
        df[f"Volatility_{window}"] = df['Close'].pct_change().rolling(window).std() * (252**0.5)
        return df

    def get_summary_statistics(self, df: pd.DataFrame):
        return {
            "mean_close": df["Close"].mean(),
            "max_close": df["Close"].max(),
            "min_close": df["Close"].min(),
            "std_close": df["Close"].std()
        }
