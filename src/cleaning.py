# src/cleaning.py

import pandas as pd

def clean_stock_data(file_path):

    df = pd.read_csv(file_path)

    print("Before Cleaning:")
    print(df.isnull().sum())

    # Remove missing values
    df.dropna(inplace=True)

    # Remove duplicates
    df.drop_duplicates(inplace=True)

    # Convert Date column
    df['Date'] = pd.to_datetime(df['Date'])

    print("\nAfter Cleaning:")
    print(df.isnull().sum())

    return df


if __name__ == "__main__":

    cleaned_df = clean_stock_data("data/AAPL.csv")

    cleaned_df.to_csv(
        "data/cleaned_AAPL.csv",
        index=False
    )

    print("\nCleaned Data Saved!")