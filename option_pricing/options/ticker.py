# Standard library imports
import datetime

# Third party imports
import requests_cache
import matplotlib.pyplot as plt
from pandas_datareader import data as wb
import yfinance as yf


class Ticker:
    """Class for fetcing data from yahoo finance."""
    
    @staticmethod
    def get_historical_data(ticker, start_date=None, end_date=None):
        """
        Fetches stock data using yfinance.

        Params:
        ticker: ticker symbol (without the exchange suffix for NSE)
        start_date: start date for getting historical data
        end_date: end date for getting historical data
        """
        try:
            # Append '.NS' for NSE stocks if no suffix is provided
            if not ('.NS' in ticker or '.BO' in ticker):
                ticker += '.NS'

            if start_date is None:
                start_date = "2022-01-01"
            if end_date is None:
                end_date = datetime.datetime.today().strftime('%Y-%m-%d')
            
            data = yf.download(ticker, start=start_date, end=end_date)
            
            if data.empty:
                print("No data found. Check ticker symbol or date range.")
                return None
            return data
        except Exception as e:
            print("Error fetching data:", e)
            return None

    @staticmethod
    def get_columns(data):
        """
        Gets dataframe columns from previously fetched stock data.
        
        Params:
        data: dataframe representing fetched data
        """
        if data is None:
            return None
        return [column for column in data.columns]

    @staticmethod
    def get_last_price(data, column_name):
        """
        Returns last available price for specified column from already fetched data.
        
        Params:
        data: dataframe representing fetched data
        column_name: name of the column in dataframe
        """
        if data is None or column_name is None:
            return None
        if column_name not in Ticker.get_columns(data):
            return None
        return data[column_name].iloc[len(data) - 1]


    @staticmethod
    def plot_data(data, ticker, column_name, ax=None):
        """
        Plots specified column values from dataframe.
        
        Params:
        data: dataframe representing fetched data
        column_name: name of the column in dataframe
        """
        if ax is None:
            fig,ax = plt.subplots()
        data[column_name].plot(ax=ax)
        ax.set_ylabel(f'{column_name}')
        ax.set_xlabel('Date')
        ax.set_title(f'Historical data for {ticker} - {column_name}')
        ax.legend(loc='best')
