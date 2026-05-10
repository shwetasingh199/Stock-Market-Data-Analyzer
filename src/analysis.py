# src/analysis.py

import pandas as pd

def calculate_daily_returns(file_path):

    df = pd.read_csv(file_path)

    # Calculate daily return
    df['Daily Return'] = df['Close'].pct_change()

    # Average return
    avg_return = df['Daily Return'].mean()

    # Volatility
    volatility = df['Daily Return'].std()

    print("\nAverage Daily Return:")
    print(avg_return)

    print("\nVolatility:")
    print(volatility)

    return df


if __name__ == "__main__":

    result = calculate_daily_returns(
        "data/cleaned_AAPL.csv"
    )

    result.to_csv(
        "data/returns_AAPL.csv",
        index=False
    )

    print("\nReturns Calculated!")