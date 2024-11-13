# Standard Python imports
from enum import Enum
from datetime import datetime, timedelta

# Third-party imports
import streamlit as st

# Local package imports
from option_pricing.options import BlackScholesModel, MonteCarloPricing, BinomialTreeModel, Ticker
from macroeco import get_all_macro_data

class OPTION_PRICING_MODEL(Enum):
    BLACK_SCHOLES = 'Black Scholes Model'
    MONTE_CARLO = 'Monte Carlo Simulation'
    BINOMIAL = 'Binomial Model'

@st.cache
def get_historical_data(ticker):
    """Getting historical data for specified ticker and caching it with Streamlit."""
    data = Ticker.get_historical_data(ticker)
    if data is not None and not data.empty:
        # Flatten MultiIndex columns if necessary
        data.columns = [col[0] if isinstance(col, tuple) else col for col in data.columns]
    return data

import pandas as pd
from datetime import datetime

def display_macro_factors():
    """Display macroeconomic factors in a structured table with centered headings and formatted values."""
    # Get today's date
    today = datetime.today().strftime("%Y-%m-%d")

    # Define macroeconomic data as a dictionary and format values
    macro_data = {
        'GDP Growth Rate': '7.6%',
        'Unemployment Rate': '7.8%',
        'Repo Rate': '6.5%',
        'CPI': '6.21%',
        'Consumer Confidence Index': '94.7 pts',
        '10-Year Treasury Yield': '6.917%'
    }

    # Convert the data to a DataFrame and add a row index starting from 1
    macro_df = pd.DataFrame(list(macro_data.items()), columns=["Factor", f"Value (as of {today})"])
    macro_df.index += 1  # Start the index from 1

    # Style the table
    styled_table = macro_df.style.set_properties(**{'text-align': 'center'}) \
                                 .set_table_styles([{'selector': 'th', 'props': [('text-align', 'center')]}])

    # Display the table with Streamlit
    st.subheader("Macroeconomic Indicators")
    st.write(styled_table)

def adjust_parameters_based_on_macro_factors():
    """Adjust model parameters based on macroeconomic factors."""
    macro_data = get_all_macro_data()
    
    # Example weights for each macroeconomic factor
    weights = {
        'GDP Growth Rate': 0.15,
        'Unemployment Rate': 0.10,
        'Repo Rate': 0.20,
        'CPI': 0.15,
        'Consumer Confidence Index': 0.20,
        '10-Year Treasury Yield': 0.20
    }
    
    # Extract values (assuming they are already in numeric form)
    gdp_growth = macro_data['GDP Growth Rate']
    unemployment_rate = macro_data['Unemployment Rate']
    repo_rate = macro_data['Repo Rate']
    cpi = macro_data['CPI']
    cci = macro_data['Consumer Confidence Index']
    treasury_yield = macro_data['10-Year Treasury Yield']

    # Adjust parameters based on weighted macroeconomic factors
    adjusted_risk_free_rate = (repo_rate * weights['Repo Rate'] + treasury_yield * weights['10-Year Treasury Yield']) / 100
    adjusted_volatility = ((cpi * weights['CPI'] + (100 - cci) * weights['Consumer Confidence Index']) / 100) / 100  # Example for volatility adjustment

    # Return adjusted parameters
    return adjusted_risk_free_rate, adjusted_volatility


# Main title
st.title('Option Pricing Application for Indian Stocks')

# User-selected model from sidebar
pricing_method = st.sidebar.radio(
    'Please select an option pricing method',
    options=[model.value for model in OPTION_PRICING_MODEL]
)

# Displaying specified model
st.subheader(f'Pricing method: {pricing_method}')

if pricing_method == OPTION_PRICING_MODEL.BLACK_SCHOLES.value:
    # Parameters for Black-Scholes model
    ticker = st.text_input('Enter NSE ticker symbol (e.g., "RELIANCE" for Reliance Industries)', 'RELIANCE')
    strike_price = st.number_input('Strike price', 300)
    base_risk_free_rate = st.slider('Base Risk-free rate (%)', 0, 100, 10)
    base_sigma = st.slider('Base Sigma (%)', 0, 100, 20)
    exercise_date = st.date_input(
        'Exercise date',
        min_value=datetime.today() + timedelta(days=1),
        value=datetime.today() + timedelta(days=365)
    )

    # Display macroeconomic factors
    display_macro_factors()
    
    if st.button(f'Calculate option price for {ticker}'):
        # Getting data for the selected ticker
        data = get_historical_data(ticker)
        if data is not None:
            st.write("Historical Data:")
            st.write(data.tail())
            Ticker.plot_data(data, ticker, 'Adj Close')
            st.pyplot()

            # Formatting selected model parameters
            spot_price = Ticker.get_last_price(data, 'Adj Close')
            days_to_maturity = (exercise_date - datetime.now().date()).days

            # Adjusting parameters based on macroeconomic factors
            adjusted_risk_free_rate, adjusted_volatility = adjust_parameters_based_on_macro_factors()
            risk_free_rate = base_risk_free_rate / 100 + adjusted_risk_free_rate  # Combine base and adjusted rates
            sigma = base_sigma / 100 + adjusted_volatility  # Combine base and adjusted volatility

            # Calculating option price
            BSM = BlackScholesModel(spot_price, strike_price, days_to_maturity, risk_free_rate, sigma)
            call_option_price = BSM.calculate_option_price('Call Option')
            put_option_price = BSM.calculate_option_price('Put Option')

            # Displaying call/put option price
            st.subheader(f'Call option price: {call_option_price}')
            st.subheader(f'Put option price: {put_option_price}')
        else:
            st.error("Failed to fetch data. Please check the ticker symbol.")


if pricing_method == OPTION_PRICING_MODEL.MONTE_CARLO.value:
    # Parameters for Monte Carlo simulation
    ticker = st.text_input('Enter NSE ticker symbol (e.g., "TCS" for TCS)', 'TCS')
    strike_price = st.number_input('Strike price', 300)
    base_risk_free_rate = st.slider('Base Risk-free rate (%)', 0, 100, 10)
    base_sigma = st.slider('Base Sigma (%)', 0, 100, 20)
    exercise_date = st.date_input(
        'Exercise date',
        min_value=datetime.today() + timedelta(days=1),
        value=datetime.today() + timedelta(days=365)
    )
    
    number_of_simulations = st.slider('Number of simulations', 100, 100000, 10000)
    num_of_movements = st.slider('Number of price movement simulations to visualize', 0, int(number_of_simulations / 10), 100)

    # Display macroeconomic factors
    display_macro_factors()

    if st.button(f'Calculate option price for {ticker}'):
        # Getting data for the selected ticker
        data = get_historical_data(ticker)
        if data is not None:
            st.write("Historical Data:")
            st.write(data.tail())
            Ticker.plot_data(data, ticker, 'Adj Close')
            st.pyplot()

            # Formatting simulation parameters
            spot_price = Ticker.get_last_price(data, 'Adj Close')
            days_to_maturity = (exercise_date - datetime.now().date()).days

            # Adjusting parameters based on macroeconomic factors
            adjusted_risk_free_rate, adjusted_volatility = adjust_parameters_based_on_macro_factors()
            risk_free_rate = base_risk_free_rate / 100 + adjusted_risk_free_rate  # Combine base and adjusted rates
            sigma = base_sigma / 100 + adjusted_volatility  # Combine base and adjusted volatility

            # Simulating stock movements
            MC = MonteCarloPricing(spot_price, strike_price, days_to_maturity, risk_free_rate, sigma, number_of_simulations)
            MC.simulate_prices()

            # Visualizing Monte Carlo Simulation
            MC.plot_simulation_results(num_of_movements)
            st.pyplot()

            # Calculating call/put option price
            call_option_price = MC.calculate_option_price('Call Option')
            put_option_price = MC.calculate_option_price('Put Option')

            # Displaying call/put option price
            st.subheader(f'Call option price: {call_option_price}')
            st.subheader(f'Put option price: {put_option_price}')
        else:
            st.error("Failed to fetch data. Please check the ticker symbol.")

if pricing_method == OPTION_PRICING_MODEL.BINOMIAL.value:
    # Parameters for Binomial Tree model
    ticker = st.text_input('Enter NSE ticker symbol (e.g., "INFY" for Infosys)', 'INFY')
    strike_price = st.number_input('Strike price', 300)
    base_risk_free_rate = st.slider('Base Risk-free rate (%)', 0, 100, 10)
    base_sigma = st.slider('Base Sigma (%)', 0, 100, 20)
    exercise_date = st.date_input(
        'Exercise date',
        min_value=datetime.today() + timedelta(days=1),
        value=datetime.today() + timedelta(days=365)
    )
    num_time_steps = st.slider('Number of time steps', 500, 10000, 1000)

    # Display macroeconomic factors
    display_macro_factors()

    if st.button(f'Calculate option price for {ticker}'):
        # Getting data for the selected ticker
        data = get_historical_data(ticker)
        if data is not None:
            st.write("Historical Data:")
            st.write(data.tail())
            Ticker.plot_data(data, ticker, 'Adj Close')
            st.pyplot()

            # Formatting simulation parameters
            spot_price = Ticker.get_last_price(data, 'Adj Close')
            days_to_maturity = (exercise_date - datetime.now().date()).days

            # Adjusting parameters based on macroeconomic factors
            adjusted_risk_free_rate, adjusted_volatility = adjust_parameters_based_on_macro_factors()
            risk_free_rate = base_risk_free_rate / 100 + adjusted_risk_free_rate  # Combine base and adjusted rates
            sigma = base_sigma / 100 + adjusted_volatility  # Combine base and adjusted volatility

            # Calculating option prices using adjusted parameters
            BOPM = BinomialTreeModel(spot_price, strike_price, days_to_maturity, risk_free_rate, sigma, num_time_steps)
            call_option_price = BOPM.calculate_option_price('Call Option')
            put_option_price = BOPM.calculate_option_price('Put Option')

            # Displaying call/put option price
            st.subheader(f'Call option price: {call_option_price}')
            st.subheader(f'Put option price: {put_option_price}')
        else:
            st.error("Failed to fetch data. Please check the ticker symbol.")

