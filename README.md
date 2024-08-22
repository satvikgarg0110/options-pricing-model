
## Introduction


This repository contains a straightforward web application designed to calculate the prices of European options. It implements three distinct methods for option pricing:


The Black-Scholes model
Monte Carlo simulation
The Binomial model


Each model has various parameters that user needs to import:  


- Ticker  
- Strike price  
- Expiry date  
- Risk-free rate  
- Volatility  


Option pricing models are implemented in [Python 3.7](https://www.python.org/downloads/release/python-377/). Latest spot price, for specified ticker, is fetched from Yahoo Finance API using [pandas-datareader](https://pandas-datareader.readthedocs.io/en/latest/). Visualization of the models through simple web app is implemented using [streamlit](https://www.streamlit.io/) library.  


When data is fetched from Yahoo Finance API using pandas-datareader, it's cached with [request-cache](https://github.com/reclosedev/requests-cache) library is sqlite db, so any subsequent testing and changes in model parameters with same underlying instrument won't result in duplicated request for fethcing already fetched data.


## Project Structure
This repository includes the following components:


demo directory: Contains .gif files showcasing examples of the Streamlit app in action.
option_pricing package: A Python package where the various option pricing models are implemented.
option_pricing_test.py script: A script with example code to test the option pricing models independently of the web app.
streamlit_app.py script: The script for the web application, which allows testing of the models using the Streamlit library.
Requirements.txt file: Lists the Python packages required for the project.
Dockerfile: Used for running the Streamlit web app in a containerized environment.
app.yaml file: Configuration file for deploying the Dockerized app on Google Cloud Platform (GCP).





