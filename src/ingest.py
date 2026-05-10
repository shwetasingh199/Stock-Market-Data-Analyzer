# src/ingest.py

import yfinance as yf
import pandas as pd

def fetch_stock_data(ticker, start_date, end_date):

    df = yf.download(
        ticker,
        start=start_date,
        end=end_date
    )

    df.reset_index(inplace=True)

    return df


if __name__ == "__main__":

    stock_data = fetch_stock_data(
        "AAPL",
        "2022-01-01",
        "2024-01-01"
    )

    print(stock_data.head())

    stock_data.to_csv("data/AAPL.csv", index=False)

    print("\nData Saved Successfully!")