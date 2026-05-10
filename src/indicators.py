# src/indicators.py

import pandas as pd

def calculate_moving_averages(file_path):

    df = pd.read_csv(file_path)

    # 20-Day Moving Average
    df['MA20'] = df['Close'].rolling(window=20).mean()

    # 50-Day Moving Average
    df['MA50'] = df['Close'].rolling(window=50).mean()

    print(df[['Close', 'MA20', 'MA50']].tail())

    return df


if __name__ == "__main__":

    df = calculate_moving_averages(
        "data/returns_AAPL.csv"
    )

    df.to_csv(
        "data/final_AAPL.csv",
        index=False
    )

    print("\nMoving Averages Added!")