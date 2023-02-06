import yfinance as yf
import pandas as pd

ticker = input("Enter Stock Ticker:")
# options = yf.Ticker(ticker).options
stock_price = yf.download(ticker, period='1mo')["Adj Close"][-1]
expiry = input("Enter Expiration Date:")
strike = float(input("Enter Strike Price:"))

print("{} last: ${:.2f}".format(ticker,stock_price))
print("")
options = yf.Ticker(ticker).option_chain(expiry)
calls = options.calls
calls['mid'] = (calls['bid'] + calls['ask']) / 2
mid = calls['mid'].loc[calls['strike'] == strike]
print("The mid-point price is ${:.2f}".format(mid.iloc[0]))
