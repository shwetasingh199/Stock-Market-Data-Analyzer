# src/visualization.py

import pandas as pd
import matplotlib.pyplot as plt

def plot_stock_data(file_path):

    df = pd.read_csv(file_path)

    plt.figure(figsize=(14,7))

    plt.plot(
        df['Close'],
        label='Closing Price'
    )

    plt.plot(
        df['MA20'],
        label='20-Day MA'
    )

    plt.plot(
        df['MA50'],
        label='50-Day MA'
    )

    plt.title("Stock Price Analysis")

    plt.xlabel("Days")

    plt.ylabel("Price")

    plt.legend()

    plt.savefig(
        "outputs/stock_analysis.png"
    )

    plt.show()


if __name__ == "__main__":

    plot_stock_data(
        "data/final_AAPL.csv"
    )
    