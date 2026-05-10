# =========================================================
# STOCK MARKET DATA ANALYZER
# Streamlit Dashboard
# =========================================================

# Run Command:
# streamlit run streamlit_app/app.py

# =========================================================
# IMPORT LIBRARIES
# =========================================================

import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Stock Market Data Analyzer",
    layout="wide"
)

# =========================================================
# TITLE
# =========================================================

st.title("📈 Stock Market Data Analyzer")

st.markdown("""
Analyze stock prices, moving averages,
daily returns, volatility, RSI,
Bollinger Bands, and trading volume
using Python & Streamlit.
""")

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.header("📊 User Input")

ticker = st.sidebar.text_input(
    "Enter Stock Ticker",
    "AAPL"
)

start_date = st.sidebar.date_input(
    "Start Date",
    pd.to_datetime("2022-01-01")
)

end_date = st.sidebar.date_input(
    "End Date",
    pd.to_datetime("today")
)

# =========================================================
# ANALYZE BUTTON
# =========================================================

if st.sidebar.button("Analyze Stock"):

    try:

        # =========================================================
        # FETCH STOCK DATA
        # =========================================================

        with st.spinner("Fetching stock data..."):

            df = yf.download(
                tickers=ticker,
                start=str(start_date),
                end=str(end_date),
                progress=False,
                auto_adjust=True
            )

        # =========================================================
        # CHECK IF DATA EXISTS
        # =========================================================

        if df.empty:

            st.error(
                "❌ No stock data found.\n\n"
                "Try:\n"
                "- AAPL\n"
                "- TSLA\n"
                "- MSFT\n"
                "- GOOGL\n"
                "- RELIANCE.NS\n"
                "- TCS.NS"
            )

        else:

            st.success("✅ Stock Data Loaded Successfully!")

            # =========================================================
            # RESET INDEX
            # =========================================================

            df.reset_index(inplace=True)

            # =========================================================
            # FIX MULTI-INDEX COLUMNS
            # =========================================================

            if isinstance(df.columns, pd.MultiIndex):

                df.columns = df.columns.get_level_values(0)

            # =========================================================
            # CONVERT TO NUMERIC
            # =========================================================

            numeric_columns = [
                'Open',
                'High',
                'Low',
                'Close',
                'Volume'
            ]

            for col in numeric_columns:

                df[col] = pd.to_numeric(
                    df[col],
                    errors='coerce'
                )

            # =========================================================
            # REMOVE NULL VALUES
            # =========================================================

            df.dropna(inplace=True)

            # =========================================================
            # MOVING AVERAGES
            # =========================================================

            df['MA20'] = df['Close'].rolling(
                window=20
            ).mean()

            df['MA50'] = df['Close'].rolling(
                window=50
            ).mean()

            # =========================================================
            # DAILY RETURNS
            # =========================================================

            df['Daily Return'] = (
                df['Close'].pct_change()
            )

            # =========================================================
            # CUMULATIVE RETURNS
            # =========================================================

            df['Cumulative Return'] = (
                1 + df['Daily Return']
            ).cumprod()

            # =========================================================
            # VOLATILITY
            # =========================================================

            df['Rolling Volatility'] = (
                df['Daily Return']
                .rolling(window=20)
                .std()
            )

            # =========================================================
            # MANUAL RSI CALCULATION
            # =========================================================

            delta = df['Close'].diff()

            gain = delta.where(
                delta > 0,
                0
            )

            loss = -delta.where(
                delta < 0,
                0
            )

            avg_gain = gain.rolling(
                window=14
            ).mean()

            avg_loss = loss.rolling(
                window=14
            ).mean()

            rs = avg_gain / avg_loss

            df['RSI'] = 100 - (
                100 / (1 + rs)
            )

            # =========================================================
            # MANUAL BOLLINGER BANDS
            # =========================================================

            df['bb_middle'] = (
                df['Close']
                .rolling(window=20)
                .mean()
            )

            std_dev = (
                df['Close']
                .rolling(window=20)
                .std()
            )

            df['bb_high'] = (
                df['bb_middle']
                + (2 * std_dev)
            )

            df['bb_low'] = (
                df['bb_middle']
                - (2 * std_dev)
            )

            # =========================================================
            # DATASET PREVIEW
            # =========================================================

            st.subheader("📋 Dataset Preview")

            st.dataframe(df.head())

            # =========================================================
            # STOCK PRICE CHART
            # =========================================================

            st.subheader(
                "📈 Stock Price & Moving Averages"
            )

            fig = go.Figure()

            # Close Price

            fig.add_trace(
                go.Scatter(
                    x=df['Date'],
                    y=df['Close'],
                    mode='lines',
                    name='Close Price'
                )
            )

            # MA20

            fig.add_trace(
                go.Scatter(
                    x=df['Date'],
                    y=df['MA20'],
                    mode='lines',
                    name='MA20'
                )
            )

            # MA50

            fig.add_trace(
                go.Scatter(
                    x=df['Date'],
                    y=df['MA50'],
                    mode='lines',
                    name='MA50'
                )
            )

            fig.update_layout(
                title=f"{ticker} Stock Analysis",
                xaxis_title="Date",
                yaxis_title="Price",
                template="plotly_dark",
                height=600
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

            # =========================================================
            # DAILY RETURNS GRAPH
            # =========================================================

            st.subheader(
                "📉 Daily Returns Analysis"
            )

            returns_fig = go.Figure()

            returns_fig.add_trace(
                go.Scatter(
                    x=df['Date'],
                    y=df['Daily Return'],
                    mode='lines',
                    name='Daily Return'
                )
            )

            returns_fig.update_layout(
                title="Daily Returns",
                xaxis_title="Date",
                yaxis_title="Returns",
                template="plotly_dark",
                height=500
            )

            st.plotly_chart(
                returns_fig,
                use_container_width=True
            )

            # =========================================================
            # VOLUME ANALYSIS
            # =========================================================

            st.subheader(
                "📊 Trading Volume Analysis"
            )

            volume_fig = go.Figure()

            volume_fig.add_trace(
                go.Bar(
                    x=df['Date'],
                    y=df['Volume'],
                    name='Volume'
                )
            )

            volume_fig.update_layout(
                title="Trading Volume",
                xaxis_title="Date",
                yaxis_title="Volume",
                template="plotly_dark",
                height=500
            )

            st.plotly_chart(
                volume_fig,
                use_container_width=True
            )

            # =========================================================
            # CUMULATIVE RETURNS
            # =========================================================

            st.subheader(
                "📈 Cumulative Returns"
            )

            cum_fig = go.Figure()

            cum_fig.add_trace(
                go.Scatter(
                    x=df['Date'],
                    y=df['Cumulative Return'],
                    mode='lines',
                    name='Cumulative Return'
                )
            )

            cum_fig.update_layout(
                title="Cumulative Returns",
                xaxis_title="Date",
                yaxis_title="Growth",
                template="plotly_dark",
                height=500
            )

            st.plotly_chart(
                cum_fig,
                use_container_width=True
            )

            # =========================================================
            # VOLATILITY GRAPH
            # =========================================================

            st.subheader(
                "📉 Rolling Volatility"
            )

            vol_fig = go.Figure()

            vol_fig.add_trace(
                go.Scatter(
                    x=df['Date'],
                    y=df['Rolling Volatility'],
                    mode='lines',
                    name='Volatility'
                )
            )

            vol_fig.update_layout(
                title="20-Day Rolling Volatility",
                xaxis_title="Date",
                yaxis_title="Volatility",
                template="plotly_dark",
                height=500
            )

            st.plotly_chart(
                vol_fig,
                use_container_width=True
            )

            # =========================================================
            # RETURNS DISTRIBUTION
            # =========================================================

            st.subheader(
                "📊 Daily Returns Distribution"
            )

            hist_fig = go.Figure()

            hist_fig.add_trace(
                go.Histogram(
                    x=df['Daily Return'],
                    nbinsx=50,
                    name='Returns Distribution'
                )
            )

            hist_fig.update_layout(
                title="Distribution of Daily Returns",
                xaxis_title="Daily Return",
                yaxis_title="Frequency",
                template="plotly_dark",
                height=500
            )

            st.plotly_chart(
                hist_fig,
                use_container_width=True
            )

            # =========================================================
            # RSI GRAPH
            # =========================================================

            st.subheader(
                "📌 RSI Indicator"
            )

            rsi_fig = go.Figure()

            rsi_fig.add_trace(
                go.Scatter(
                    x=df['Date'],
                    y=df['RSI'],
                    mode='lines',
                    name='RSI'
                )
            )

            rsi_fig.update_layout(
                title="Relative Strength Index (RSI)",
                xaxis_title="Date",
                yaxis_title="RSI",
                template="plotly_dark",
                height=500
            )

            st.plotly_chart(
                rsi_fig,
                use_container_width=True
            )

            # =========================================================
            # BOLLINGER BANDS
            # =========================================================

            st.subheader(
                "📌 Bollinger Bands"
            )

            bb_fig = go.Figure()

            bb_fig.add_trace(
                go.Scatter(
                    x=df['Date'],
                    y=df['Close'],
                    mode='lines',
                    name='Close Price'
                )
            )

            bb_fig.add_trace(
                go.Scatter(
                    x=df['Date'],
                    y=df['bb_high'],
                    mode='lines',
                    name='Upper Band'
                )
            )

            bb_fig.add_trace(
                go.Scatter(
                    x=df['Date'],
                    y=df['bb_low'],
                    mode='lines',
                    name='Lower Band'
                )
            )

            bb_fig.update_layout(
                title="Bollinger Bands",
                xaxis_title="Date",
                yaxis_title="Price",
                template="plotly_dark",
                height=500
            )

            st.plotly_chart(
                bb_fig,
                use_container_width=True
            )

            # =========================================================
            # RISK ANALYSIS
            # =========================================================

            volatility = float(
                df['Daily Return'].std()
            )

            highest_price = float(
                df['High'].max()
            )

            lowest_price = float(
                df['Low'].min()
            )

            st.subheader(
                "📊 Risk Analysis"
            )

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "Volatility",
                    f"{volatility:.4f}"
                )

            with col2:

                st.metric(
                    "🔺 Highest Price",
                    f"${highest_price:.2f}"
                )

            with col3:

                st.metric(
                    "🔻 Lowest Price",
                    f"${lowest_price:.2f}"
                )

            # =========================================================
            # STATISTICAL SUMMARY
            # =========================================================

            st.subheader(
                "📌 Statistical Summary"
            )

            st.write(
                df.describe()
            )

            # =========================================================
            # DOWNLOAD CSV
            # =========================================================

            csv = df.to_csv(index=False)

            st.download_button(
                label="⬇ Download Processed CSV",
                data=csv,
                file_name=f"{ticker}_analysis.csv",
                mime="text/csv"
            )

            # =========================================================
            # FINAL MESSAGE
            # =========================================================

            st.success(
                "✅ Stock Analysis Completed Successfully!"
            )

    except Exception as e:

        st.error(
            f"❌ Error: {e}"
        )