# Standard Python imports
from enum import Enum
from datetime import datetime, timedelta
import streamlit as st
import matplotlib.pyplot as plt
import yfinance as yf

from option_pricing import BlackScholesModel, MonteCarloPricing, BinomialTreeModel

# Define option pricing models
class OPTION_PRICING_MODEL(Enum):
    BLACK_SCHOLES = 'Black Scholes Model'
    MONTE_CARLO = 'Monte Carlo Simulation'
    BINOMIAL = 'Binomial Model'

# Cache the historical data for performance improvement
@st.cache_data
def get_historical_data(ticker):
    """Fetch historical data from yfinance."""
    start = '2020-01-01'
    end = datetime.now().strftime('%Y-%m-%d')
    data = yf.download(ticker, start=start, end=end)
    return data

# Function to plot stock data
def plot_data(data, ticker):
    fig, ax = plt.subplots()
    ax.plot(data['Adj Close'])
    ax.set_title(f'{ticker} Adjusted Close Price')
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    st.pyplot(fig)

# Main title
st.title('Option Pricing App')

# Sidebar selection for model
pricing_method = st.sidebar.radio('Select option pricing method', options=[model.value for model in OPTION_PRICING_MODEL])

# Display selected pricing model
st.subheader(f'Pricing method: {pricing_method}')

if pricing_method == OPTION_PRICING_MODEL.BLACK_SCHOLES.value:
    # Parameters for Black-Scholes model
    ticker = st.text_input('Ticker symbol', 'AAPL')
    strike_price = st.number_input('Strike price', 300)
    risk_free_rate = st.slider('Risk-free rate (%)', 0, 100, 10) / 100
    sigma = st.slider('Sigma (%)', 0, 100, 20) / 100
    exercise_date = st.date_input('Exercise date', min_value=datetime.today() + timedelta(days=1), value=datetime.today() + timedelta(days=365))
    
    if st.button(f'Calculate option price for {ticker}'):
        # Fetch historical data
        data = get_historical_data(ticker)
        if data.empty:
            st.error("No data fetched for the ticker. Please check the symbol.")
        else:
            st.write(data.tail())  # Display last 5 rows
            plot_data(data, ticker)

            # Extract last price and calculate time to maturity
            spot_price = data['Adj Close'].iloc[-1]
            days_to_maturity = (exercise_date - datetime.now().date()).days

            # Calculate option price using Black-Scholes (assuming you have the BlackScholesModel class implemented)
            BSM = BlackScholesModel(spot_price, strike_price, days_to_maturity, risk_free_rate, sigma)
            call_option_price = BSM.calculate_option_price('Call Option')
            put_option_price = BSM.calculate_option_price('Put Option')

            st.subheader(f'Call option price: {call_option_price}')
            st.subheader(f'Put option price: {put_option_price}')

elif pricing_method == OPTION_PRICING_MODEL.MONTE_CARLO.value:
    # Parameters for Monte Carlo simulation
    ticker = st.text_input('Ticker symbol', 'AAPL')
    strike_price = st.number_input('Strike price', 300)
    risk_free_rate = st.slider('Risk-free rate (%)', 0, 100, 10) / 100
    sigma = st.slider('Sigma (%)', 0, 100, 20) / 100
    exercise_date = st.date_input('Exercise date', min_value=datetime.today() + timedelta(days=1), value=datetime.today() + timedelta(days=365))
    number_of_simulations = st.slider('Number of simulations', 100, 100000, 10000)
    num_of_movements = st.slider('Number of price movement simulations to visualize ', 0, int(number_of_simulations / 10), 100)

    if st.button(f'Calculate option price for {ticker}'):
        data = get_historical_data(ticker)
        if data.empty:
            st.error("No data fetched for the ticker. Please check the symbol.")
        else:
            st.write(data.tail())  # Display last 5 rows
            plot_data(data, ticker)

            spot_price = data['Adj Close'].iloc[-1]
            days_to_maturity = (exercise_date - datetime.now().date()).days

            # Monte Carlo Simulation (assuming you have MonteCarloPricing class implemented)
            MC = MonteCarloPricing(spot_price, strike_price, days_to_maturity, risk_free_rate, sigma, number_of_simulations)
            MC.simulate_prices()
            MC.plot_simulation_results(num_of_movements)

            call_option_price = MC.calculate_option_price('Call Option')
            put_option_price = MC.calculate_option_price('Put Option')

            st.subheader(f'Call option price: {call_option_price}')
            st.subheader(f'Put option price: {put_option_price}')

elif pricing_method == OPTION_PRICING_MODEL.BINOMIAL.value:
    ticker = st.text_input('Ticker symbol', 'AAPL')
    strike_price = st.number_input('Strike price', 300)
    risk_free_rate = st.slider('Risk-free rate (%)', 0, 100, 10) / 100
    sigma = st.slider('Sigma (%)', 0, 100, 20) / 100
    exercise_date = st.date_input('Exercise date', min_value=datetime.today() + timedelta(days=1), value=datetime.today() + timedelta(days=365))
    number_of_time_steps = st.slider('Number of time steps', 5000, 100000, 15000)

    if st.button(f'Calculate option price for {ticker}'):
        data = get_historical_data(ticker)
        if data.empty:
            st.error("No data fetched for the ticker. Please check the symbol.")
        else:
            st.write(data.tail())  # Display last 5 rows
            plot_data(data, ticker)

            spot_price = data['Adj Close'].iloc[-1]
            days_to_maturity = (exercise_date - datetime.now().date()).days

            # Binomial Model (assuming you have BinomialTreeModel class implemented)
            BOPM = BinomialTreeModel(spot_price, strike_price, days_to_maturity, risk_free_rate, sigma, number_of_time_steps)
            call_option_price = BOPM.calculate_option_price('Call Option')
            put_option_price = BOPM.calculate_option_price('Put Option')

            st.subheader(f'Call option price: {call_option_price}')
            st.subheader(f'Put option price: {put_option_price}')
