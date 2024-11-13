from option_pricing import BlackScholesModel, MonteCarloPricing, BinomialTreeModel
import yfinance as yf
import matplotlib.pyplot as plt

# Fetching stock data from yfinance
data = yf.download('TSLA', start='2020-01-01', end='2023-12-31')

# Displaying the columns of the data
print(data.columns)

# Fetching the last adjusted close price
print(data['Adj Close'].iloc[-1])

# Plotting the data
plt.plot(data['Adj Close'])
plt.title('TSLA Adjusted Close Price')
plt.xlabel('Date')
plt.ylabel('Price')
plt.show()

# Black-Scholes model testing
BSM = BlackScholesModel(100, 100, 365, 0.1, 0.2)
print(BSM.calculate_option_price('Call Option'))
print(BSM.calculate_option_price('Put Option'))

# Binomial model testing
BOPM = BinomialTreeModel(100, 100, 365, 0.1, 0.2, 15000)
print(BOPM.calculate_option_price('Call Option'))
print(BOPM.calculate_option_price('Put Option'))

# Monte Carlo simulation testing
MC = MonteCarloPricing(100, 100, 365, 0.1, 0.2, 10000)
MC.simulate_prices()
print(MC.calculate_option_price('Call Option'))
print(MC.calculate_option_price('Put Option'))
MC.plot_simulation_results(20)
