# test_macro_data.py
from macroeco import (
    get_gdp_growth_world_bank,
    get_cpi_world_bank,
    get_consumer_confidence_world_bank,
    get_10_year_treasury_yield,
    get_unemployment_rate_world_bank,
    get_repo_rate_nasdaq,
    get_all_macro_data
)

def test_individual_functions():
    """Test each function individually and print results."""
    print("Testing Individual Functions:\n")
    
    print("GDP Growth Rate:", get_gdp_growth_world_bank())
    print("CPI (Consumer Price Index):", get_cpi_world_bank())
    print("Consumer Confidence Index:", get_consumer_confidence_world_bank())
    print("10-Year Treasury Yield:", get_10_year_treasury_yield())
    print("Unemployment Rate:", get_unemployment_rate_world_bank())
    print("Repo Rate:", get_repo_rate_nasdaq())
    print("\n")

def test_all_macro_data():
    """Test the combined macro data retrieval function."""
    print("Testing get_all_macro_data:\n")
    macro_data = get_all_macro_data()
    for key, value in macro_data.items():
        print(f"{key}: {value if value is not None else 'Data not available'}")

if __name__ == "__main__":
    print("Running API Data Retrieval Tests...\n")
    test_individual_functions()
    test_all_macro_data()
