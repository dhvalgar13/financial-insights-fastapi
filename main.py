from fastapi import FastAPI, Query
from finance_utils import FinancialAnalyzer
from typing import Optional
import asyncio

app = FastAPI()
analyzer = FinancialAnalyzer()

@app.get("/")
async def root():
    return {"message": "Welcome to Financial Analysis API"}

@app.get("/treasury/yield-spread")
async def yield_spread(long: str = "10 Yr", short: str = "2 Yr"):
    df = await analyzer.fetch_treasury_data()
    result = analyzer.calculate_yield_spread(df, long=long, short=short)
    return result.tail(10).to_dict(orient="index")

@app.get("/stocks/data")
def stock_data(ticker: str = "^GSPC", period: str = "1y"):
    df = analyzer.fetch_stock_data(ticker, period)
    return df.tail(5).reset_index().to_dict(orient="records")

@app.get("/stocks/sma")
def sma_data(ticker: str = "^GSPC", window: int = 50):
    df = analyzer.fetch_stock_data(ticker)
    df = analyzer.add_sma(df, window)
    return df.tail(5).reset_index().to_dict(orient="records")

@app.get("/stocks/volatility")
def volatility_data(ticker: str = "^GSPC", window: int = 20):
    df = analyzer.fetch_stock_data(ticker)
    df = analyzer.add_volatility(df, window)
    return df.tail(5).reset_index().to_dict(orient="records")

@app.get("/stocks/summary")
def summary_data(ticker: str = "^GSPC"):
    df = analyzer.fetch_stock_data(ticker)
    summary = analyzer.get_summary_statistics(df)
    return summary
