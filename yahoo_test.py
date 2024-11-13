import yfinance as yf
import streamlit as st
from datetime import datetime

# Streamlit app title
st.title('Yahoo Finance Data Test with yfinance')

# User input for ticker symbol
ticker = st.text_input('Enter ticker symbol', 'AAPL')

# Start and end dates
start = datetime(2020, 1, 1)
end = datetime.now()

if st.button(f'Fetch data for {ticker}'):
    try:
        # Fetch data using yfinance
        data = yf.download(ticker, start=start, end=end)
        if data.empty:
            st.error("No data fetched. Please check the ticker symbol.")
        else:
            st.write(data.tail())  # Display last 5 rows
    except Exception as e:
        st.error(f"Error fetching data: {e}")
