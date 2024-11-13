# macroeconomic_data.py

def get_gdp_growth():
    """Return India's GDP growth rate."""
    return 7.6  # in percentage

def get_unemployment_rate():
    """Return India's Unemployment Rate."""
    return 7.8  # in percentage

def get_repo_rate():
    """Return RBI Repo Rate."""
    return 6.5  # in percentage

def get_cpi():
    """Return India's Consumer Price Index (CPI)."""
    return 6.21  # in percentage

def get_consumer_confidence_index():
    """Return India's Consumer Confidence Index (CCI)."""
    return 94.7  # points, September 2024

def get_10_year_treasury_yield():
    """Return India 10-Year Bond Yield."""
    return 6.917  # in percentage

def get_all_macro_data():
    """Return all macroeconomic data as a dictionary."""
    return {
        'GDP Growth Rate': get_gdp_growth(),
        'Unemployment Rate': get_unemployment_rate(),
        'Repo Rate': get_repo_rate(),
        'CPI': get_cpi(),
        'Consumer Confidence Index': get_consumer_confidence_index(),
        '10-Year Treasury Yield': get_10_year_treasury_yield()
    }
