# Black-Scholes Option Pricing Tool

This project is a web-based application developed using **Streamlit** that provides an interactive interface for option pricing based on the **Black-Scholes model**.  

It allows users to calculate option prices, implied volatility, and Greek values, with real-time visualizations to enhance understanding of option behavior under various conditions.

Run the tool: https://black-scholes-option-pricer.streamlit.app/

## Features

1. **Option Price Calculation**: 
   - Users can input option parameters (spot price, strike price, time to maturity, risk-free rate, and volatility) to compute the price of both **call** and **put** options.
   - Plots are generated to visualize how the option price varies with changes in spot, volatility, and time to maturity.

2. **Implied Volatility Calculation**: 
   - Given an option's type, market price, and other parameters, the tool approximates the implied volatility using Newton's method.
   
3. **Greeks Calculation**: 
   - The tool computes the Greeks (Delta, Gamma, Theta, Vega, Rho, Vanna, Volga) based on the input.
   - Plots are generated to visualize how the Greeks vary with the spot price.

## Libraries Used

- **pandas**
- **numpy**
- **scipy**
- **streamlit**
